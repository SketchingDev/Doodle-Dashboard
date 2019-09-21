import json
from abc import abstractmethod

from doodledashboard.component import NamedComponent


class Message:
    """
    Represents a textual entity from a data feed.
    """

    # @todo Update Messages to use dictionaries instead of text
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

    @source_name.setter
    def source_name(self, source_name):
        self._source_name = source_name

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


# @todo Should secret be passed to DataFeedConfig instead
# @body By passing it to the config then all configuration/validation of the data-feed happens in one place
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

    def get_messages(self):
        messages = self.get_latest_messages()
        for message in messages:
            message.source_name = self.name

        return messages

    @property
    def secret_store(self):
        return self._secret_store

    @secret_store.setter
    def secret_store(self, secret_store):
        self._secret_store = secret_store
