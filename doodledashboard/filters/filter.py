from abc import ABC, abstractmethod


class MessageFilter(ABC):
    def __init__(self):
        self._successor = None

    @abstractmethod
    def filter(self, text_entity):
        pass
