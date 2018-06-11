import yaml

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

    def __init__(self, components_loader=None):
        self._filter_creator = RootConfigSection()
        self._handler_creator = RootConfigSection()
        self._data_feed_creator = RootConfigSection()
        self._available_displays = []

        if components_loader:
            components_loader.configure(self)

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

    def read_yaml(self, config_yaml):
        config = yaml.safe_load(config_yaml)

        if not config:
            raise InvalidConfigurationException("Configuration file is empty")

        return Dashboard(
            self._parse_interval(config),
            self._parse_display(config),
            self._parse_data_feeds(config),
            self._parse_notifications(config)
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
        self._check_not_empty(dashboard)

    @staticmethod
    def _check_handlers_supports_display(dashboard):
        display = dashboard.get_display()
        for notification in dashboard.get_notifications():
            handler = notification.get_handler()
            requirements = handler.display_requirements

            for requirement in requirements:
                if not isinstance(display, requirement):
                    raise InvalidConfigurationException(
                        "Display %s does not have required functionality for notification %s" % (display, notification)
                    )

    @staticmethod
    def _check_not_empty(dashboard):
        if not dashboard:
            raise InvalidConfigurationException("Configuration is empty")

    @staticmethod
    def _check_has_display(dashboard):
        if not dashboard.get_display():
            raise InvalidConfigurationException("No display defined. Check that the ID you provided is valid.")


class InvalidConfigurationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
