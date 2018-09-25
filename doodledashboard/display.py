from abc import ABC, abstractmethod


class Display(ABC):

    @abstractmethod
    def draw(self, notification):
        """
        Called by the dashboard when the display should try and draw the notification.
        :param notification: The notification to draw that is of a type returned by `get_supported_notifications()`
        """

    @staticmethod
    @abstractmethod
    def get_supported_notifications():
        """
        This method is called when the consumer of the display wants to know what notification it supports.
        :return: An array of all the notification types that are supported by the display.
        """

    @staticmethod
    @abstractmethod
    def get_config_factory():
        """
        :return: The factory class used to create the display from the configuration.
        """
