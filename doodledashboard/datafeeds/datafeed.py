import json
from abc import ABC, abstractmethod


class Message:
    """
    Represents a single_config textual entity from a data feed.
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

    def __init__(self):
        self._secret_store = None

    @abstractmethod
    def get_latest_messages(self):
        """
        Called by the dashboard when it is ready to process new messages.
        :return: An array of the latest messages from the datafeed
        """

    @staticmethod
    @abstractmethod
    def get_config_factory():
        """
        :return: The factory class used to create the datafeed from the
        configuration.
        """

    def set_secret_store(self, secret_store):
        self._secret_store = secret_store

    def get_secret_store(self):
        return self._secret_store
