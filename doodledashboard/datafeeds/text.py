from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import DataFeed, TextEntity, DataFeedConfigSection


class TextFeed(DataFeed):
    def __init__(self, text):
        DataFeed.__init__(self)
        if isinstance(text, list):
            self._text = text
        else:
            self._text = [text]

    def get_latest_entities(self):
        return [TextEntity(text, self) for text in self._text]

    def get_text(self):
        return self._text

    def __str__(self):
        return "Text"


class TextFeedSection(DataFeedConfigSection):
    def __init__(self):
        DataFeedConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "text"

    def create_item(self, config_section):
        if "text" not in config_section:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return TextFeed(config_section["text"])
