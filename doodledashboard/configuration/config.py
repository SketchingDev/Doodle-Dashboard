from functools import reduce

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
    def create(self, config_section):
        pass

    def add(self, successor):
        if not self._successor:
            self._successor = successor
        else:
            self._successor.add(successor)


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

    def __init__(self, creator_container):
        self._creator_container = creator_container

    @staticmethod
    def try_create(section, creators):
        for creator in creators:
            if creator.can_create(section):
                return creator.create(section)

        return None

    def read_yaml(self, yaml_configs):
        configs = []
        for yaml_config in yaml_configs:
            try:
                config = yaml.safe_load(yaml_config)
                if config:
                    configs.append(config)
            except YAMLError as err:
                raise YamlParsingError(err, yaml_config)

        dashboards = []
        for config in configs:
            dashboards.append(Dashboard(
                self._parse_interval(config),
                self._parse_display(config),
                self._parse_data_feeds(config),
                self._parse_notifications(config)
            ))

        return reduce(DashboardConfigReader.merge, dashboards, Dashboard())

    @staticmethod
    def merge(accum_value: Dashboard, x: Dashboard):
        if x.get_interval() is not None:
            accum_value.set_interval(x.get_interval())

        if x.get_display():
            accum_value.set_display(x.get_display())

        accum_value.add_data_feeds(x.get_data_feeds())
        accum_value.add_notifications(x.get_notifications())

        return accum_value

    def _parse_interval(self, config):
        return config["interval"] if "interval" in config else None

    def _parse_display(self, config):
        display = self.try_create(config, self._creator_container.get_display_creators())

        if not display and "display" in config:
            raise DisplayNotFound(config["display"])

        return display

    def _parse_data_feeds(self, config):
        if "data-feeds" in config:
            for element in config["data-feeds"] or []:
                data_feed = self.try_create(element, self._creator_container.get_data_feed_creators())
                if data_feed:
                    yield data_feed

    def _parse_notifications(self, config):
        if "notifications" in config:
            for notification_element in config["notifications"] or []:
                notification = self._parse_notification(notification_element)
                if not notification:
                    pass  # TODO Handle notification not being created from notification configuration

                if notification:
                    yield notification

    def _parse_notification(self, notification_section):
        notification = self.try_create(notification_section, self._creator_container.get_notification_creators())

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
        updater = self.try_create(updater_section, self._creator_container.get_notification_updater_creators())

        if updater and "filter-messages" in updater_section:
            message_filters = self._parse_message_filters(updater_section["filter-messages"])
            updater.add_message_filters(message_filters)

        return updater

    def _parse_message_filters(self, message_filters_section):
        for section in message_filters_section:
            message_filter = self.try_create(section, self._creator_container.get_filter_creators())
            if message_filter:
                yield message_filter


class ValidateDashboard:

    def validate(self, dashboard):
        self._check_display_supports_notification(dashboard)

    @staticmethod
    def _check_display_supports_notification(dashboard):
        display = dashboard.get_display()

        for notification in dashboard.get_notifications():
            if notification.__class__ not in display.get_supported_notifications():
                raise DisplayDoesNotSupportNotification(display, notification)


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


class DisplayNotFound(InvalidConfigurationException):
    def __init__(self, display_id):
        self.display_id = display_id


class DisplayDoesNotSupportNotification(InvalidConfigurationException):
    def __init__(self, display, notification):
        self.display = display
        self.notification = notification
