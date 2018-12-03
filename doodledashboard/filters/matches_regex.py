import re

from doodledashboard.component import ComponentConfig, FilterConfig, MissingRequiredOptionException
from doodledashboard.filters.filter import MessageFilter


class MatchesRegexFilter(MessageFilter):

    def __init__(self, regex):
        MessageFilter.__init__(self)
        self._regex = re.compile(regex, re.IGNORECASE)

    def filter(self, message):
        return True if self._regex.search(message.text) else False

    @property
    def pattern(self):
        return self._regex.pattern


class MatchesRegexFilterConfig(ComponentConfig, FilterConfig):

    @staticmethod
    def get_id():
        return "message-matches-regex"

    def create(self, options):
        if "pattern" not in options:
            raise MissingRequiredOptionException("Expected 'pattern' option to exist")

        return MatchesRegexFilter(str(options["text"]))
