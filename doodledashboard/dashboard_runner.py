import itertools
import logging
import time
import click


class Dashboard:
    def __init__(self, interval, display, data_feeds, notifications):
        self._interval = interval
        self._display = display
        self._data_feeds = data_feeds
        self._notifications = notifications

    def get_interval(self):
        return self._interval

    def get_display(self):
        return self._display

    def get_data_feeds(self):
        return self._data_feeds

    def get_notifications(self):
        return self._notifications


class Notification:
    def __init__(self, handler):
        self._handler = handler
        self._filter_chain = None
        self._logger = logging.getLogger("doodledashboard")

    def set_filter_chain(self, filter_chain):
        self._filter_chain = filter_chain

    def handle_messages(self, display, messages):
        filtered_messages = self._filter_messages(messages)

        self._logger.debug("Messages after filters: %s", [filtered_messages])

        self._handler.update(filtered_messages)
        self._handler.draw(display)

    def _filter_messages(self, messages):
        if self._filter_chain:
            return self._filter_chain.filter(messages)
        else:
            return messages

    def __str__(self):
        return "Displays messages using: %s" % str(self._handler)


class DashboardRunner:
    def __init__(self, dashboard):
        self._logger = logging.getLogger("doodledashboard.Dashboard")
        self._dashboard = dashboard

    def run(self):
        messages = []
        for notification in itertools.cycle(self._dashboard.get_notifications()):

            if self._is_at_beginning(notification):
                self._logger.info("At beginning of notification cycle, will poll data sources")
                messages = self._collect_all_messages(self._dashboard.get_data_feeds())
                self._logger.info("%s messages collected" % len(messages))

            notification.handle_messages(self._dashboard.get_display(), messages)
            time.sleep(self._dashboard.get_interval())

    def _is_at_beginning(self, notification):
        return notification is self._dashboard.get_notifications()[0]

    @staticmethod
    def _collect_all_messages(repositories):
        messages = []
        for repository in repositories:
            messages += repository.get_latest_messages()

        return messages
