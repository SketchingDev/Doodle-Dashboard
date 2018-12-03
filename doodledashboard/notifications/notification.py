from abc import ABC, abstractmethod


class Notification(ABC):
    """
    A notification creates an output (text, image etc) from a batch of messages that it is provided.
    """

    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def create(self, messages):
        output = self.create_output(messages)
        output.name = self.name

        return output

    @abstractmethod
    def create_output(self, messages):
        """
        Creates an output based on the content of the messages.
        If no output can be created from the messages, then None can be returned
        :param messages: Latest messages from polling data-sources
        :return: Output or None
        """

    @abstractmethod
    def get_output_types(self):
        """
        :return: Return an array of the types of outputs this notification produces. This is used to check the
        display that's been configured can handle all the types of outputs the notification could produce.
        """


class FilteredNotification(Notification):
    """
    Filters messages prior to them being passed to the notification
    """

    def __init__(self, notification, message_filters):
        super().__init__()
        self._notification = notification
        self._message_filters = message_filters

    def create_output(self, messages):
        filtered_messages = self.filter_messages(messages)
        return self._notification.create_output(filtered_messages)

    def get_output_types(self):
        return self._notification.get_output_types()

    def filter_messages(self, messages):
        return list(filter(self._keep_message, messages))

    def _keep_message(self, message):
        for f in self._message_filters:
            if f.filter(message) is False:
                return False
        return True
