from abc import abstractmethod, ABC
from pkg_resources import iter_entry_points

from doodledashboard.configuration.config import InvalidConfigurationException
from doodledashboard.datafeeds.datetime import DateTimeFeed
from doodledashboard.datafeeds.rss import RssFeed
from doodledashboard.datafeeds.slack import SlackFeed
from doodledashboard.datafeeds.text import TextFeed
from doodledashboard.display import Display
from doodledashboard.filters.contains_text import ContainsTextFilter
from doodledashboard.filters.matches_regex import MatchesRegexFilter
from doodledashboard.notifications import TextNotification, ImageNotification, \
    ImageWithTextNotification, ColourNotification
from doodledashboard.updaters.image.image import ImageNotificationUpdater
from doodledashboard.updaters.text.text import TextNotificationUpdater


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

    # TODO These don't need to be abstract, look into being able to override one or two

    @abstractmethod
    def _find_displays(self):
        return []

    @abstractmethod
    def _find_data_feeds(self):
        return []

    @abstractmethod
    def _find_notifications(self):
        return []

    @abstractmethod
    def _find_notification_updaters(self):
        return []

    @abstractmethod
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

    def _find_data_feeds(self):
        return []

    def _find_notifications(self):
        return []

    def _find_notification_updaters(self):
        return []

    def _find_filters(self):
        return []


class ExternalPackageLoader(ComponentsLoader):

    _DISPLAYS_GROUP_NAME = "doodledashboard.customdisplays"

    def _find_displays(self):
        for entry_point in iter_entry_points(ExternalPackageLoader._DISPLAYS_GROUP_NAME):
            yield entry_point.load()

    def _find_data_feeds(self):
        return []

    def _find_notifications(self):
        return []

    def _find_notification_updaters(self):
        return []

    def _find_filters(self):
        return []


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


class InternalPackageLoader(ComponentsLoader):

    def _find_displays(self):
        return []

    def _find_data_feeds(self):
        return [
            RssFeed,
            SlackFeed,
            DateTimeFeed,
            TextFeed
        ]

    def _find_notifications(self):
        return [
            TextNotification,
            ImageNotification,
            ImageWithTextNotification,
            ColourNotification
        ]

    def _find_notification_updaters(self):
        return [
            TextNotificationUpdater,
            ImageNotificationUpdater
        ]

    def _find_filters(self):
        return [
            MatchesRegexFilter,
            ContainsTextFilter
        ]
