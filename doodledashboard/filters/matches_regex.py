import re

from doodledashboard.component import FilterCreator, MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.filter import MessageFilter


class MatchesRegexFilter(MessageFilter):

    def __init__(self, regex):
        MessageFilter.__init__(self)
        self._regex = re.compile(regex, re.IGNORECASE)

    def filter(self, message: Message):
        return True if self._regex.search(message.text) else False

    @property
    def pattern(self):
        return self._regex.pattern


class MatchesRegexFilterCreator(FilterCreator):

    @staticmethod
    def get_id() -> str:
        return "message-matches-regex"

    def create(self, options: dict, secret_store: dict) -> MatchesRegexFilter:
        if "pattern" not in options:
            raise MissingRequiredOptionException("Expected 'pattern' option to exist")

        return MatchesRegexFilter(str(options["text"]))
