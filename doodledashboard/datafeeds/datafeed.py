import json

from doodledashboard.configuration.config import ConfigSection


class TextEntity:

    """
    Represents a single textual entity from a data feed.
    """

    def __init__(self, text, source=None):
        """
        :param text: Entity's text
        :param source: Source of the entity, which is converted to a string via `str()` to produce the source name
        """

        self._text = text
        self._source_name = str(source) if source else ""

    def get_source_name(self):
        return self._source_name

    def get_text(self):
        return self._text


class TextEntityJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TextEntity):
            return {
                "text": obj.get_text(),
                "source": str(obj.get_source_name())
            }

        return json.JSONEncoder.default(self, obj)


class DataFeed:
    def __init__(self):
        pass

    def get_latest_entities(self):
        raise NotImplementedError("Implement this method")


class DataFeedConfigSection(ConfigSection):
    def __init__(self):
        ConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "source" in config_section and self.creates_for_id(config_section["source"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")
