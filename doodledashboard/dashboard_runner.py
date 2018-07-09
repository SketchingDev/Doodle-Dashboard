import time

import logging


class Dashboard:
    def __init__(self, interval=None, display=None, data_feeds=None, notifications=None):
        self._interval = interval
        self._display = display
        self._data_feeds = data_feeds or []
        self._notifications = notifications or []

    def get_interval(self):
        return self._interval

    def set_interval(self, interval):
        self._interval = interval

    def get_display(self):
        return self._display

    def set_display(self, display):
        self._display = display

    def get_data_feeds(self):
        return self._data_feeds

    def add_data_feeds(self, data_feeds):
        self._data_feeds += data_feeds

    def get_notifications(self):
        return self._notifications

    def add_notifications(self, notifications):
        self._notifications += notifications


class DashboardRunner:
    def __init__(self, dashboard):
        self._logger = logging.getLogger("doodledashboard.Dashboard")
        self._dashboard = dashboard

    def cycle(self):
        """
        Cycles through notifications with latest results from data feeds, pausing after each notification.
        """
        messages = self.poll_datafeeds()
        self.process_notifications(messages)

        self.draw_notifications()

    def poll_datafeeds(self):
        messages = []
        for feed in self._dashboard.get_data_feeds():
            messages += feed.get_latest_messages()

        return messages

    def draw_notifications(self):
        notifications = self._dashboard.get_notifications()
        display = self._dashboard.get_display()
        interval = self._dashboard.get_interval()

        for notification in notifications:
            display.draw(notification)
            time.sleep(interval)

    def process_notifications(self, messages):
        for notification in self._dashboard.get_notifications():
            for message in messages:
                notification.update(message)
