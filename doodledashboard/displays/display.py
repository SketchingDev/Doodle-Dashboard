from abc import abstractmethod

from doodledashboard.component import NamedComponent


class Display(NamedComponent):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def draw(self, notification_output):
        """
        Called by the dashboard when the display should try and draw the notification.

        Implementations should block the thread whilst the display is showing a notification, as soon as the thread is
        unblocked then all data-sources will be polled.

        :param notification_output: The notification to draw that is of a type returned by
        `get_supported_notifications()`
        """

    @staticmethod
    @abstractmethod
    def get_supported_notifications():
        """
        This method is called when the consumer of the display wants to know what notification it supports.
        :return: An array of all the notification types that are supported by the display.
        """
