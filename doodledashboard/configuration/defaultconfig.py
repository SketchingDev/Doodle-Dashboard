import pkgutil

from doodledashboard.configuration.config import RootCreator
from doodledashboard.datafeeds.datetime import DateTimeFeedConfigCreator
from doodledashboard.datafeeds.rss import RssFeedConfigCreator
from doodledashboard.datafeeds.slack import SlackRepositoryConfigCreator
from doodledashboard.displays.consoledisplay import ConsoleDisplayConfigCreator
from doodledashboard.filters import MessageMatchesRegexTextFilterCreator, MessageContainsTextFilterCreator
from doodledashboard.handlers.image.image import ImageMessageHandlerConfigCreator, FileDownloader
from doodledashboard.handlers.text.text import TextHandlerConfigCreator


class DefaultConfiguration:
    @staticmethod
    def set_creators(state_storage, dashboard_config):
        dashboard_config.set_display_creator(DefaultConfiguration._get_display_creators())
        dashboard_config.set_data_source_creators(DefaultConfiguration._get_data_source_creators())
        dashboard_config.set_handler_creators(DefaultConfiguration._get_handler_creators(state_storage))
        dashboard_config.set_filter_creators(DefaultConfiguration._get_filter_creators())

    @staticmethod
    def _get_display_creators():
        creator = RootCreator()
        creator.add(ConsoleDisplayConfigCreator())

        papirus_loader = pkgutil.find_loader('papirus')
        if papirus_loader:
            from doodledashboard.displays.papirusdisplay import PapirusDisplayConfigCreator
            creator.add(PapirusDisplayConfigCreator())

        return creator

    @staticmethod
    def _get_data_source_creators():
        creator = RootCreator()
        creator.add(RssFeedConfigCreator())
        creator.add(SlackRepositoryConfigCreator())
        creator.add(DateTimeFeedConfigCreator())

        return creator

    @staticmethod
    def _get_handler_creators(key_value_store):
        creator = RootCreator()
        creator.add(ImageMessageHandlerConfigCreator(key_value_store, FileDownloader()))
        creator.add(TextHandlerConfigCreator(key_value_store))

        return creator

    @staticmethod
    def _get_filter_creators():
        creator = RootCreator()
        creator.add(MessageMatchesRegexTextFilterCreator())
        creator.add(MessageContainsTextFilterCreator())

        return creator
