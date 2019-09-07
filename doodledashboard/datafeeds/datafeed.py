import json
from abc import ABC, abstractmethod


class Message:
    """
    Represents a textual entity from a data feed.
    """

    def __init__(self, text, source_name=''):
        """
        :param text: Entity's text
        :param source_name: Name of the message source
        """

        self._text = text
        self._source_name = source_name

    @property
    def source_name(self):
        return self._source_name

    @property
    def text(self):
        return self._text


class MessageJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return {
                "text": obj.text,
                "source": str(obj.source_name)
            }

        return json.JSONEncoder.default(self, obj)


class DataFeed(ABC):

    def __init__(self):
        self._secret_store = {}
        self.name = ""

    @abstractmethod
    def get_latest_messages(self):
        """
        Called by the dashboard when it is ready to process new messages.
        :return: An array of the latest messages from the datafeed
        """

    # @todo Remove duplication of `name` getter/setter.
    # @body Duplication could be removed by moving into common NamedComponent class, although I think this might create
    # an odd circular dependency loop
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def secret_store(self):
        return self._secret_store

    @secret_store.setter
    def secret_store(self, secret_store):
        self._secret_store = secret_store
