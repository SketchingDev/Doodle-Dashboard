from abc import ABC
from pkg_resources import iter_entry_points

from doodledashboard.configuration.config import InvalidConfigurationException
from doodledashboard.display import Display


class ComponentsLoader(ABC):

    def populate(self, container):
        def extract(components):
            return [component.get_config_factory() for component in components]

        container.add_display_creators(
            extract(self._find_displays())
        )
        container.add_data_feed_creators(
            extract(self._find_data_feeds())
        )
        container.add_notification_creators(
            extract(self._find_notifications())
        )
        container.add_notification_updater_creators(
            extract(self._find_notification_updaters())
        )
        container.add_filter_creators(
            extract(self._find_filters())
        )

    def _find_displays(self):
        return []

    def _find_data_feeds(self):
        return []

    def _find_notifications(self):
        return []

    def _find_notification_updaters(self):
        return []

    def _find_filters(self):
        return []


def validate_displays(displays):
    for display in displays:
        if not issubclass(display, Display):
            raise InvalidConfigurationException(
                "Display loaded does not implement Display base class. Contact the Display's creator"
            )
    return displays


class StaticDisplayLoader(ComponentsLoader):
    displays = []

    def _find_displays(self):
        return StaticDisplayLoader.displays


class ExternalPackageLoader(ComponentsLoader):

    _DISPLAYS_GROUP_NAME = "doodledashboard.custom.displays"
    _FILTERS_GROUP_NAME = "doodledashboard.custom.filters"
    _DATA_FEED_GROUP_NAME = "doodledashboard.custom.datafeeds"
    _NOTIFICATIONS_GROUP_NAME = "doodledashboard.custom.notifications"
    _NOTIFICATION_UPDATERS_GROUP_NAME = "doodledashboard.custom.notification.updaters"

    @staticmethod
    def _find_entry_points_by_group(group_name):
        for entry_point in iter_entry_points(group_name):
            yield entry_point.load()

    def _find_displays(self):
        return self._find_entry_points_by_group(ExternalPackageLoader._DISPLAYS_GROUP_NAME)

    def _find_data_feeds(self):
        return self._find_entry_points_by_group(ExternalPackageLoader._DATA_FEED_GROUP_NAME)

    def _find_notifications(self):
        return self._find_entry_points_by_group(ExternalPackageLoader._NOTIFICATIONS_GROUP_NAME)

    def _find_notification_updaters(self):
        return self._find_entry_points_by_group(ExternalPackageLoader._NOTIFICATION_UPDATERS_GROUP_NAME)

    def _find_filters(self):
        return self._find_entry_points_by_group(ExternalPackageLoader._FILTERS_GROUP_NAME)


class CreatorsContainer:

    def __init__(self):
        self._filter_creators = []
        self._notification_creators = []
        self._notification_updater_creators = []
        self._data_feed_creators = []
        self._display_creators = []

    def add_filter_creators(self, creators):
        self._filter_creators += creators

    def add_notification_creators(self, creators):
        self._notification_creators += creators

    def add_notification_updater_creators(self, creators):
        self._notification_updater_creators += creators

    def add_data_feed_creators(self, creators):
        self._data_feed_creators += creators

    def add_display_creators(self, creators):
        self._display_creators += creators

    def get_filter_creators(self):
        return self._filter_creators

    def get_notification_creators(self):
        return self._notification_creators

    def get_notification_updater_creators(self):
        return self._notification_updater_creators

    def get_data_feed_creators(self):
        return self._data_feed_creators

    def get_display_creators(self):
        return self._display_creators
