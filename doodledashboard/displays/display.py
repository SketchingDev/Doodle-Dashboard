from abc import ABC, abstractmethod


class Display(ABC):

    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @abstractmethod
    def draw(self, notification):
        """
        Called by the dashboard when the display should try and draw the notification.

        Implementations should block the thread whilst the display is showing a notification, as soon as the thread is
        unblocked then all data-sources will be polled.

        :param notification: The notification to draw that is of a type returned by `get_supported_notifications()`
        """

    @staticmethod
    @abstractmethod
    def get_supported_notifications():
        """
        This method is called when the consumer of the display wants to know what notification it supports.
        :return: An array of all the notification types that are supported by the display.
        """
