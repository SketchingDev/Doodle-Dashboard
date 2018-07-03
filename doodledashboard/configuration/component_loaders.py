from abc import abstractmethod, ABC
from pkg_resources import iter_entry_points

from doodledashboard.configuration.config import InvalidConfigurationException
from doodledashboard.datafeeds.datetime import DateTimeFeedConfig
from doodledashboard.datafeeds.rss import RssFeedConfig
from doodledashboard.datafeeds.slack import SlackFeedConfig
from doodledashboard.datafeeds.text import TextFeedConfig
from doodledashboard.display import Display
from doodledashboard.filters.contains_text import ContainsTextFilterConfig
from doodledashboard.filters.matches_regex import MatchesRegexFilterConfig
from doodledashboard.notifications import TextNotificationConfig, ImageNotificationConfig, \
    ImageWithTextNotificationConfig, ColourNotificationConfig
from doodledashboard.updaters.image.image import ImageNotificationUpdaterConfig
from doodledashboard.updaters.text.text import TextNotificationUpdaterConfig


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


class InternalPackageLoader(ComponentsLoader):

    def configure(self, dashboard_config):
        dashboard_config.add_data_feed_creators(InternalPackageLoader._find_data_feed_creators())
        dashboard_config.add_notification_creators(InternalPackageLoader._find_notification_creators())
        dashboard_config.add_notification_updater_creators(InternalPackageLoader._find_notification_updater_creators())
        dashboard_config.add_filter_creators(InternalPackageLoader._find_filter_creators())

    @staticmethod
    def _find_data_feed_creators():
        return [
            RssFeedConfig(),
            SlackFeedConfig(),
            DateTimeFeedConfig(),
            TextFeedConfig()
        ]

    @staticmethod
    def _find_notification_creators():
        return [
            TextNotificationConfig(),
            ImageNotificationConfig(),
            ImageWithTextNotificationConfig(),
            ColourNotificationConfig()
        ]

    @staticmethod
    def _find_notification_updater_creators():
        return [
            TextNotificationUpdaterConfig(),
            ImageNotificationUpdaterConfig()
        ]

    @staticmethod
    def _find_filter_creators():
        return [
            MatchesRegexFilterConfig(),
            ContainsTextFilterConfig()
        ]
