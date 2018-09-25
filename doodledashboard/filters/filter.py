from abc import ABC, abstractmethod


class MessageFilter(ABC):
    def __init__(self):
        self._successor = None

    @abstractmethod
    def filter(self, message):
        """
        :param message: Message to filter
        :return: True if the message should be kept, otherwise false.
        """

    @staticmethod
    @abstractmethod
    def get_config_factory():
        """
        :return: The factory class used to create the message filter from the configuration.
        """
