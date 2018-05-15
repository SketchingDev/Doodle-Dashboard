from datetime import datetime

from doodledashboard.datafeeds.datafeed import DataFeed, TextEntity, DataFeedConfigSection


class DateTimeFeed(DataFeed):
    def __init__(self):
        DataFeed.__init__(self)

    def get_latest_entities(self):

        date_time = datetime.now().isoformat(timespec="minutes")
        return [TextEntity(str(date_time), self)]

    def __str__(self):
        return "Date/Time (e.g. 2002-12-25T00:00)"


class DateTimeFeedSection(DataFeedConfigSection):
    def __init__(self):
        DataFeedConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "datetime"

    def create_item(self, config_section):
        return DateTimeFeed()
