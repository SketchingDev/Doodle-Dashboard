import pkgutil

from doodledashboard.datafeeds.datetime import DateTimeFeedConfigCreator
from doodledashboard.datafeeds.rss import RssFeedConfigCreator
from doodledashboard.datafeeds.slack import SlackRepositoryConfigCreator
from doodledashboard.displays.consoledisplay import ConsoleDisplayConfigCreator
from doodledashboard.filters import MessageMatchesRegexTextFilterCreator, MessageContainsTextFilterCreator
from doodledashboard.handlers.image.image import ImageMessageHandlerConfigCreator, FileDownloader
from doodledashboard.handlers.text.text import TextHandlerConfigCreator


class DefaultConfigCreators:

    def __init__(self, state_storage):
        self._state_storage = state_storage

    def configure(self, dashboard_config):
        dashboard_config.add_display_creators(DefaultConfigCreators._get_display_creators())
        dashboard_config.add_data_source_creators(DefaultConfigCreators._get_data_source_creators())
        dashboard_config.add_handler_creators(DefaultConfigCreators._get_handler_creators(self._state_storage))
        dashboard_config.add_filter_creators(DefaultConfigCreators._get_filter_creators())

    @staticmethod
    def _get_display_creators():
        creators = [ConsoleDisplayConfigCreator()]

        papirus_loader = pkgutil.find_loader('papirus')
        if papirus_loader:
            from doodledashboard.displays.papirusdisplay import PapirusDisplayConfigCreator
            creators.append(PapirusDisplayConfigCreator())

        return creators

    @staticmethod
    def _get_data_source_creators():
        return [
            RssFeedConfigCreator(),
            SlackRepositoryConfigCreator(),
            DateTimeFeedConfigCreator()
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
            MessageMatchesRegexTextFilterCreator(),
            MessageContainsTextFilterCreator()
        ]
