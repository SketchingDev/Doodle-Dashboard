from doodledashboard.configuration.config import MissingRequiredOptionException, ConfigSection
from doodledashboard.filters.filter import MessageFilter


class ContainsTextFilter(MessageFilter):
    def __init__(self, text):
        MessageFilter.__init__(self)
        self._text = text

    def filter(self, text_entity):
        return self._text in text_entity.get_text()

    def remove_text(self, text_entity):
        return text_entity.get_text() \
            .replace(self._text, "") \
            .strip()

    def get_text(self):
        return self._text

    @staticmethod
    def get_config_factory():
        return ContainsTextFilterConfig()


class ContainsTextFilterConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "message-contains-text"

    def create(self, config_section):
        if "text" not in config_section:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return ContainsTextFilter(str(config_section["text"]))
