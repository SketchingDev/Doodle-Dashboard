import logging


class Dashboard:
    def __init__(self, display=None, data_feeds=None, notifications=None):
        self._display = display
        self._data_feeds = data_feeds or []
        self._notifications = notifications or []

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display

    @property
    def data_feeds(self):
        return self._data_feeds

    def add_data_feeds(self, data_feeds):
        self._data_feeds += data_feeds

    @property
    def notifications(self):
        return self._notifications

    def add_notifications(self, notifications):
        self._notifications += notifications


class DashboardRunner:

    def __init__(self, dashboard):
        self._logger = logging.getLogger(__name__)
        self._dashboard = dashboard

    def cycle(self):
        """
        Cycles through notifications with latest results from data feeds.
        """
        messages = self.poll_datafeeds()
        notifications = self.process_notifications(messages)

        self.draw_notifications(notifications)

    def poll_datafeeds(self):
        messages = []
        for feed in self._dashboard.data_feeds:
            messages += feed.get_latest_messages()

        return messages

    def process_notifications(self, messages):
        for notification in self._dashboard.notifications:
            yield notification.create(messages)

    def draw_notifications(self, notifications):
        display = self._dashboard.display

        for notification in notifications:
            display.draw(notification)


class DashboardValidator:

    def validate(self, dashboard):
        self._check_display_supports_notification(dashboard)

    @staticmethod
    def _check_display_supports_notification(dashboard: Dashboard):
        supported_notifications = dashboard.display.get_supported_notifications()

        for notification in dashboard.notifications:
            output_types = notification.get_output_types()
            for output_type in output_types:
                if output_type not in supported_notifications:
                    raise DisplayDoesNotSupportNotification(dashboard.display, notification, output_type)


class ValidationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DisplayDoesNotSupportNotification(ValidationException):
    def __init__(self, display, notification, output_type_not_supported):
        super().__init__("Display '%s' does not support output type '%s'" % (display.name, output_type_not_supported))
        self.display = display
        self.notification = notification
        self.output_type_not_supported = output_type_not_supported
