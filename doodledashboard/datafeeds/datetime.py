from datetime import datetime
from typing import List

from doodledashboard.component import DataFeedCreator
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class DateTimeFeed(DataFeed):

    def get_latest_messages(self) -> List[Message]:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [Message(date_time)]

    def __str__(self) -> str:
        return "Date/Time (e.g. 2002-12-25 00:00)"


class DateTimeFeedCreator(DataFeedCreator):

    @staticmethod
    def get_id() -> str:
        return "datetime"

    def create(self, options: dict, secret_store: dict) -> DateTimeFeed:
        return DateTimeFeed()
