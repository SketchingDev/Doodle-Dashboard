import yaml

from functools import reduce

from doodledashboard.component import ComponentType
from doodledashboard.dashboard import Dashboard
from doodledashboard.notifications.notification import FilteredNotification


class DashboardMerger:

    def __init__(self, default=None):
        self._default_dashboard = default or Dashboard()

    def merge(self, dashboards):
        return reduce(DashboardMerger.dashboard_reduce, dashboards, self._default_dashboard)

    @staticmethod
    def dashboard_reduce(accum_value: Dashboard, x: Dashboard):
        if x.display:
            accum_value.display = x.display

        accum_value.add_data_feeds(x.data_feeds)
        accum_value.add_notifications(x.notifications)

        return accum_value


class ComponentConfigParser:
    """
    Parses a the most common configuration of:
        {
            'type': '<component ID>'
            'options:
                'key1': '<value>'
                'key2': '<value>'
        }
    """

    def __init__(self, section_component_configs):
        self._component_configs = section_component_configs

    def parse(self, config):
        """
            Parses the section of configuration pertaining to a component
            :param config: dict of specific config section
            :return:
        """

        if "type" not in config:
            raise InvalidConfigurationException("The dashboard configuration has not defined a 'type'. %s" % config)

        component_type = config["type"]
        component_config = self._get_config_by_id(self._component_configs, component_type)

        if not component_config:
            raise ComponentNotFoundForType(component_type)

        options = config.get("options", {})
        component = self._parse_item(component_config, options, config)
        component.name = config.get("name", "")
        return component

    def _parse_item(self, component_config, options, root_config):
        return component_config.create(options)

    @staticmethod
    def _get_config_by_id(component_configs, component_id):
        for config_parser in component_configs:
            if config_parser.get_id() == component_id:
                return config_parser
        return None


class NotificationComponentsConfigParser(ComponentConfigParser):

    def __init__(self, notification_configs, filter_parser):
        super().__init__(notification_configs)
        self._filter_parser = filter_parser

    def _parse_item(self, component_config, options, root_config):
        notification = component_config.create(options)

        if "filters" in root_config:
            filters = self._parse_filters(root_config["filters"])
            return FilteredNotification(notification, filters)
        else:
            return notification

    def _parse_filters(self, filters_config):
        return [self._filter_parser.parse(section) for section in filters_config]


class DashboardConfigReader:

    def __init__(self, component_configs_loader, secrets):
        self._dashboard_merger = DashboardMerger()
        self._component_configs_loader = component_configs_loader
        self._secret_store = secrets

        self._initialise_parsers()

    def _initialise_parsers(self):
        display_configs = self._component_configs_loader.load_by_type(ComponentType.DISPLAY)
        self._display_config_section_parser = ComponentConfigParser(display_configs)

        data_feed_configs = self._component_configs_loader.load_by_type(ComponentType.DATA_FEED)
        self._data_feed_config_section_parser = ComponentConfigParser(data_feed_configs)

        filter_configs = self._component_configs_loader.load_by_type(ComponentType.FILTER)
        filter_parser = ComponentConfigParser(filter_configs)

        notification_configs = \
            self._component_configs_loader.load_by_type(ComponentType.NOTIFICATION)
        self._notification_config_section_parser = NotificationComponentsConfigParser(
            notification_configs,
            filter_parser
        )

    def read_yaml(self, yaml_configs):
        dashboards = []

        for yaml_config in yaml_configs:
            try:
                config = yaml.safe_load(yaml_config)
            except yaml.YAMLError as err:
                raise ConfigYamlParsingError(err, yaml_config)

            dashboards.append(self._create_dashboard(config))

        return self._dashboard_merger.merge(dashboards)

    def _create_dashboard(self, config):
        config = config["dashboard"]
        if not config:
            config = {}

        display = None
        if "display" in config:
            try:
                display = self._display_config_section_parser.parse(config["display"])
            except ComponentNotFoundForType as ex:
                raise DisplayNotFound(ex.component_type)

        data_feeds = [
            self._data_feed_config_section_parser.parse(section) for section in config.get("data-feeds", [])
        ]
        for feed in data_feeds:
            feed.secret_store = self._secret_store

        notifications = [
            self._notification_config_section_parser.parse(section) for section in config.get("notifications", [])
        ]

        return Dashboard(display, data_feeds, notifications)


class InvalidConfigurationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ComponentNotFoundForType(InvalidConfigurationException):
    def __init__(self, component_type):
        super().__init__("Component not found for type '%s'" % component_type)
        self.component_type = component_type


class EmptyConfiguration(InvalidConfigurationException):
    def __init__(self, configuration_files):
        super().__init__("Configuration files are empty: %s" % configuration_files)
        self.configuration_files = configuration_files


class ConfigYamlParsingError(InvalidConfigurationException):
    def __init__(self, parsing_exception, config):
        super().__init__("Error parsing YAML file %s due to %s" % (config, parsing_exception))
        self.parsing_exception = parsing_exception
        self.config = config


class DisplayNotFound(InvalidConfigurationException):
    def __init__(self, display_id):
        super().__init__("Display %s not found" % display_id)
        self.display_id = display_id
