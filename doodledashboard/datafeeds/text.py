from doodledashboard.component import MissingRequiredOptionException, DataFeedConfig, ComponentConfig
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

    @property
    def text(self):
        return self._text

    def __str__(self):
        return "Text"


class TextFeedConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "text"

    def create(self, options):
        if "text" not in options:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return TextFeed(options["text"])
