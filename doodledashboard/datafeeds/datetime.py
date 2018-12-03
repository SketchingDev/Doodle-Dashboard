from datetime import datetime

from doodledashboard.component import DataFeedConfig, ComponentConfig
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class DateTimeFeed(DataFeed):
    def __init__(self):
        DataFeed.__init__(self)

    def get_latest_messages(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [Message(date_time, self)]

    def __str__(self):
        return "Date/Time (e.g. 2002-12-25 00:00)"

    @staticmethod
    def get_config_factory():
        return DateTimeFeedConfig()


class DateTimeFeedConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "datetime"

    def create(self, options):
        return DateTimeFeed()
