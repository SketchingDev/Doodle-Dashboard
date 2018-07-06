import json
from abc import ABC, abstractmethod


class Message:
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


class MessageJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return {
                "text": obj.get_text(),
                "source": str(obj.get_source_name())
            }

        return json.JSONEncoder.default(self, obj)


class DataFeed(ABC):

    @abstractmethod
    def get_latest_messages(self):
        return []

    @staticmethod
    @abstractmethod
    def get_config_factory():
        return None
