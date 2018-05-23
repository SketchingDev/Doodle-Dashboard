import pkgutil

from doodledashboard.datafeeds.datetime import DateTimeFeedSection
from doodledashboard.datafeeds.rss import RssFeedSection
from doodledashboard.datafeeds.slack import SlackFeedSection
from doodledashboard.displays.consoledisplay import ConsoleDisplayConfigCreator
from doodledashboard.filters.contains_text import ContainsTextFilterSection
from doodledashboard.filters.matches_regex import MatchesRegexFilterSection
from doodledashboard.handlers.image.image import ImageMessageHandlerConfigCreator, FileDownloader
from doodledashboard.handlers.text.text import TextHandlerConfigCreator


class FullConfigCollection:

    def __init__(self, state_storage):
        self._state_storage = state_storage

    def configure(self, dashboard_config):
        dashboard_config.add_display_creators(FullConfigCollection._get_display_creators())
        dashboard_config.add_data_feed_creators(FullConfigCollection._get_data_source_creators())
        dashboard_config.add_handler_creators(FullConfigCollection._get_handler_creators(self._state_storage))
        dashboard_config.add_filter_creators(FullConfigCollection._get_filter_creators())

    @staticmethod
    def _get_display_creators():
        creators = [ConsoleDisplayConfigCreator()]

        papirus_loader = pkgutil.find_loader("papirus")
        if papirus_loader:
            from doodledashboard.displays.papirusdisplay import PapirusDisplayConfigCreator
            creators.append(PapirusDisplayConfigCreator())

        return creators

    @staticmethod
    def _get_data_source_creators():
        return [
            RssFeedSection(),
            SlackFeedSection(),
            DateTimeFeedSection()
        ]

    @staticmethod
    def _get_handler_creators(key_value_store):
        return [
            ImageMessageHandlerConfigCreator(key_value_store, FileDownloader()),
            TextHandlerConfigCreator(key_value_store)
        ]

    @staticmethod
    def _get_filter_creators():
        return [
            MatchesRegexFilterSection(),
            ContainsTextFilterSection()
        ]


class DatafeedConfigCollection:

    def __init__(self):
        pass

    def configure(self, dashboard_config):
        dashboard_config.add_data_feed_creators(FullConfigCollection._get_data_source_creators())

    @staticmethod
    def _get_data_source_creators():
        return [
            RssFeedSection(),
            SlackFeedSection(),
            DateTimeFeedSection()
        ]
