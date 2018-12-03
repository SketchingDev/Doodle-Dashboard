from abc import ABC, abstractmethod


class MessageFilter(ABC):
    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @abstractmethod
    def filter(self, message):
        """
        :param message: Message to filter
        :return: True if the message should be kept, otherwise false.
        """
