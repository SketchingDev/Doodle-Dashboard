from doodledashboard.configuration.config import MissingRequiredOptionException, ConfigSection
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class TextFeed(DataFeed):
    def __init__(self, text):
        DataFeed.__init__(self)
        if isinstance(text, list):
            self._text = text
        else:
            self._text = [text]

    def get_latest_messages(self):
        return [Message(text, self) for text in self._text]

    def get_text(self):
        return self._text

    def __str__(self):
        return "Text"

    @staticmethod
    def get_config_factory():
        return TextFeedConfig()


class TextFeedConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "source", "text"

    def create(self, config_section):
        if "text" not in config_section:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return TextFeed(config_section["text"])
