from datetime import datetime

from doodledashboard.datafeeds.repository import Repository, MessageModel, RepositoryConfigCreator


class DateTimeFeed(Repository):
    def __init__(self):
        Repository.__init__(self)

    def get_latest_messages(self):

        date_time = datetime.now().isoformat(timespec="minutes")
        return [MessageModel(str(date_time))]

    def __str__(self):
        return "Date/Time (e.g. 2002-12-25T00:00)"


class DateTimeFeedConfigCreator(RepositoryConfigCreator):
    def __init__(self):
        RepositoryConfigCreator.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "datetime"

    def create_item(self, config_section):
        return DateTimeFeed()
