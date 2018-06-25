import yaml
from yaml import YAMLError
from doodledashboard.dashboard_runner import Notification, Dashboard


class ConfigSection:
    def __init__(self):
        self._successor = None

    def can_create(self, config_section):
        raise NotImplementedError("Implement this method")

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")

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
    def can_create(self, config_section):
        return False

    def create_item(self, config_section):
        pass


class FilterConfigSection(ConfigSection):
    def __init__(self):
        ConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "type" in config_section and self.creates_for_id(config_section["type"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")


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
        self._handler_creator = RootConfigSection()
        self._data_feed_creator = RootConfigSection()
        self._available_displays = []

    def add_filter_creators(self, creators):
        self._add_creator_to_chain(self._filter_creator, creators)

    def add_handler_creators(self, creators):
        self._add_creator_to_chain(self._handler_creator, creators)

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
        # DataSourceConfigSection
        if "data-feeds" in config:
            data_source_elements = config["data-feeds"]

        return self._create_items(self._data_feed_creator, data_source_elements)

    def _parse_notifications(self, config):
        notifications = []

        # NotificationsConfigSection
        if "notifications" in config:
            for notification_element in config["notifications"] or []:

                handler = self._handler_creator.create(notification_element)
                if handler:
                    notification = Notification(handler)

                    entity_filters = self._extract_entity_filters_from_notification(notification_element)
                    if entity_filters:
                        notification.set_filters(entity_filters)

                    notifications.append(notification)

        return notifications

    def _extract_entity_filters_from_notification(self, notification_element):
        entity_filters = []

        # FilterChainConfigSection
        if "filter-chain" in notification_element:
            filter_chain_elements = notification_element["filter-chain"]

            for filter_element in filter_chain_elements:
                entity_filter = self._filter_creator.create(filter_element)
                if entity_filter:
                    entity_filters.append(entity_filter)

        return entity_filters

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
        self._check_handlers_supports_display(dashboard)
        # self._check_not_empty(dashboard)

    @staticmethod
    def _check_handlers_supports_display(dashboard):
        display = dashboard.get_display()
        for notification in dashboard.get_notifications():

            handler = notification.get_handler()
            if not handler.supports_display(display):
                raise NotificationDoesNotSupportDisplay(display, handler)

    # @staticmethod
    # def _check_not_empty(dashboard):
    #     if not dashboard:
    #         raise InvalidConfigurationException("Configuration is empty")

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


class NotificationDoesNotSupportDisplay(InvalidConfigurationException):
    def __init__(self, display, handler):
        self.display = display
        self.handler = handler

    def get_missing_requirements(self):
        requirements = self.handler.display_requirements

        missing_requirements = []
        for requirement in requirements:
            if not isinstance(self.display, requirement):
                missing_requirements.append(requirement)

        return missing_requirements
