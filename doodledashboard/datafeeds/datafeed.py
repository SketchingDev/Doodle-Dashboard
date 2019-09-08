import json
from abc import abstractmethod

from doodledashboard.component import NamedComponent


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


class DataFeed(NamedComponent):

    def __init__(self):
        super().__init__()
        self._secret_store = {}

    @abstractmethod
    def get_latest_messages(self):
        """
        Called by the dashboard when it is ready to process new messages.
        :return: An array of the latest messages from the datafeed
        """

    @property
    def secret_store(self):
        return self._secret_store

    @secret_store.setter
    def secret_store(self, secret_store):
        self._secret_store = secret_store
