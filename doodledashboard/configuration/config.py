import yaml
from abc import ABC, abstractmethod
from yaml import YAMLError

from doodledashboard.dashboard_runner import Dashboard


class ConfigSection(ABC):
    def __init__(self):
        self._successor = None

    @property
    @abstractmethod
    def id_key_value(self):
        pass

    def can_create(self, config_section):
        id_key = self.id_key_value[0]
        id_value = self.id_key_value[1]

        return id_key in config_section and id_value == config_section[id_key]

    @abstractmethod
    def create_item(self, config_section):
        pass

    def add(self, successor):
        if not self._successor:
            self._successor = successor
        else:
            self._successor.add(successor)

    def create(self, config_section):
        if self.can_create(config_section):
            return self.create_item(config_section)
        elif self._successor:
            return self._successor.create(config_section)
        else:
            return None


class RootConfigSection(ConfigSection):
    @property
    def id_key_value(self):
        return "", ""

    def can_create(self, config_section):
        return False

    def create_item(self, config_section):
        pass


class HandlerCreationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MissingRequiredOptionException(HandlerCreationException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DashboardConfigReader:
    """
    Validation
    ---
    There are two types of validation:
    1. The definition of a filter, handler or display. When a ConfigCreator creates a section it will validate
       the parameters being passed into that section i.e. passing an invalid regex into the regex filter.
    2. Validation of the entire configuration i.e. is a display missing
    """
    _FIVE_SECONDS = 5

    def __init__(self):
        self._filter_creator = RootConfigSection()
        self._data_feed_creator = RootConfigSection()
        self._notification_creators = RootConfigSection()
        self._notification_updater_creators = RootConfigSection()
        self._available_displays = []

    def add_filter_creators(self, creators):
        self._add_creator_to_chain(self._filter_creator, creators)

    def add_notification_creators(self, creators):
        self._add_creator_to_chain(self._notification_creators, creators)

    def add_notification_updater_creators(self, creators):
        self._add_creator_to_chain(self._notification_updater_creators, creators)

    def add_data_feed_creators(self, creators):
        self._add_creator_to_chain(self._data_feed_creator, creators)

    def add_available_displays(self, displays):
        self._available_displays += displays

    @staticmethod
    def _add_creator_to_chain(chain, creators):
        for creator in creators:
            chain.add(creator)

    def read_yaml(self, yaml_configs):
        def merge_two_dicts(x, y):
            """Given two dicts, merge them into a new dict as a shallow copy."""
            z = x.copy()
            z.update(y)
            return z

        combined_config = {}
        for yaml_config in yaml_configs:
            try:
                config = yaml.safe_load(yaml_config)
                config = config if config else {}
                combined_config = merge_two_dicts(config, combined_config)
            except YAMLError as err:
                raise YamlParsingError(err, yaml_config)

        if not combined_config:
            raise EmptyConfiguration(yaml_configs)

        return Dashboard(
            self._parse_interval(combined_config),
            self._parse_display(combined_config),
            self._parse_data_feeds(combined_config),
            self._parse_notifications(combined_config)
        )

    def _parse_interval(self, config):
        return config["interval"] if "interval" in config else DashboardConfigReader._FIVE_SECONDS

    def _parse_display(self, config):
        display_id = config["display"] if "display" in config else None

        for display in self._available_displays:
            if display.get_id() == display_id:
                return display()

        return None

    def _parse_data_feeds(self, config):
        data_source_elements = []
        if "data-feeds" in config:
            data_source_elements = config["data-feeds"]

        return self._create_items(self._data_feed_creator, data_source_elements)

    def _parse_notifications(self, config):
        notifications = []

        if "notifications" in config:
            for notification_element in config["notifications"] or []:
                notification = self._parse_notification(notification_element)
                if not notification:
                    pass  # TODO Handle notification not being created from notification configuration

                if notification:
                    notifications.append(notification)

        return notifications

    def _parse_notification(self, notification_section):
        notification = self._notification_creators.create(notification_section)

        if notification and "update-with" in notification_section:
            updater = self._parse_updater(notification_section["update-with"])
            if not updater:
                    # TODO Handle the updater not being created as the notification won't behave as expected
                    # * Throw exception (could be a typo) * Output warning and don't load the notification (allows for
                    # graceful degradation of configs for future updates)
                    pass
            notification.set_updater(updater)

        return notification

    def _parse_updater(self, updater_section):
        updater = self._notification_updater_creators.create(updater_section)

        if updater and "filter-messages" in updater_section:
            message_filters = self._parse_message_filters(updater_section["filter-messages"])
            updater.add_message_filters(message_filters)

        return updater

    def _parse_message_filters(self, message_filters_section):
        message_filters = []

        for section in message_filters_section:
            message_filter = self._filter_creator.create(section)
            if message_filter:
                message_filters.append(message_filter)

        return message_filters

    @staticmethod
    def _create_items(creator_chain, config_elements):
        creation = []
        for element in config_elements or []:
            repository = creator_chain.create(element)
            if repository:
                creation.append(repository)

        return creation


class ValidateDashboard:

    def validate(self, dashboard):
        self._check_has_display(dashboard)
        self._check_display_supports_notification(dashboard)

    @staticmethod
    def _check_display_supports_notification(dashboard):
        display = dashboard.get_display()

        for notification in dashboard.get_notifications():
            if notification.__class__ not in display.get_supported_notifications():
                raise DisplayDoesNotSupportNotification(display, notification)

    @staticmethod
    def _check_has_display(dashboard):
        if not dashboard.get_display():
            raise ConfigurationMissingDisplay()


class InvalidConfigurationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EmptyConfiguration(InvalidConfigurationException):
    def __init__(self, configuration_files):
        self.configuration_files = configuration_files


class YamlParsingError(InvalidConfigurationException):
    def __init__(self, parsing_exception, config):
        self.parsing_exception = parsing_exception
        self.config = config


class ConfigurationMissingDisplay(InvalidConfigurationException):
    def __init__(self):
        pass


class DisplayDoesNotSupportNotification(InvalidConfigurationException):
    def __init__(self, display, notification):
        self.display = display
        self.notification = notification
