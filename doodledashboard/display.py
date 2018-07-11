from abc import ABC, abstractmethod


class Display(ABC):

    @abstractmethod
    def draw(self, notification):
        pass

    @staticmethod
    @abstractmethod
    def get_supported_notifications():
        return []

    @staticmethod
    @abstractmethod
    def get_config_factory():
        return None
