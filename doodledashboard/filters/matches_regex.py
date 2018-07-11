import re

from doodledashboard.configuration.config import MissingRequiredOptionException, ConfigSection
from doodledashboard.filters.filter import MessageFilter


class MatchesRegexFilter(MessageFilter):

    def __init__(self, regex):
        MessageFilter.__init__(self)
        self._regex = re.compile(regex, re.IGNORECASE)

    def filter(self, text_entity):
        return True if self._regex.search(text_entity.get_text()) else False

    def get_pattern(self):
        return self._regex.pattern

    @staticmethod
    def get_config_factory():
        return MatchesRegexFilterConfig()


class MatchesRegexFilterConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "message-matches-regex"

    def create(self, config_section):
        if "pattern" not in config_section:
            raise MissingRequiredOptionException("Expected 'pattern' option to exist")

        return MatchesRegexFilter(str(config_section["pattern"]))
