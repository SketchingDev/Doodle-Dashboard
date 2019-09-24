from abc import abstractmethod

from doodledashboard.component import NamedComponent
from doodledashboard.datafeeds.datafeed import Message


class MessageFilter(NamedComponent):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def filter(self, message: Message) -> bool:
        """
        :param message: Message to filter
        :return: True if the message should be kept, otherwise false.
        """
