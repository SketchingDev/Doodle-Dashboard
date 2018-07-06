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
    @abstractmethod
    def configure(self, dashboard_config):
        pass


def validate_displays(displays):
    for display in displays:
        if not issubclass(display, Display):
            raise InvalidConfigurationException(
                "Display loaded does not implement Display base class. Contact the Display's creator"
            )
    return displays


# TODO Can be removed
class StaticDisplayLoader(ComponentsLoader):
    displays = []

    def configure(self, dashboard_config):
        dashboard_config.add_available_displays(StaticDisplayLoader.displays)


class ExternalPackageLoader(ComponentsLoader):

    _DISPLAYS_GROUP_NAME = "doodledashboard.customdisplays"

    def configure(self, dashboard_config):
        dashboard_config.add_available_displays(ExternalPackageLoader._find_displays())

    @staticmethod
    def _find_displays():
        displays = []
        for entry_point in iter_entry_points(ExternalPackageLoader._DISPLAYS_GROUP_NAME):
            displays.append(entry_point.load())

        return displays


def extract_creators(find_func):
    def wrapper():
        return [thing.get_config_factory() for thing in find_func()]

    return wrapper


class InternalPackageLoader(ComponentsLoader):

    def configure(self, dashboard_config):
        dashboard_config.add_data_feed_creators(InternalPackageLoader._find_data_feeds())
        dashboard_config.add_notification_creators(InternalPackageLoader._find_notifications())
        dashboard_config.add_notification_updater_creators(InternalPackageLoader._find_notification_updaters())
        dashboard_config.add_filter_creators(InternalPackageLoader._find_filters())

    @staticmethod
    @extract_creators
    def _find_data_feeds():
        return [
            RssFeed,
            SlackFeed,
            DateTimeFeed,
            TextFeed
        ]

    @staticmethod
    @extract_creators
    def _find_notifications():
        return [
            TextNotification,
            ImageNotification,
            ImageWithTextNotification,
            ColourNotification
        ]

    @staticmethod
    @extract_creators
    def _find_notification_updaters():
        return [
            TextNotificationUpdater,
            ImageNotificationUpdater
        ]

    @staticmethod
    @extract_creators
    def _find_filters():
        return [
            MatchesRegexFilter,
            ContainsTextFilter
        ]
