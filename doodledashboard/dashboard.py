import itertools
import logging
import time


class Dashboard:
    _FIVE_SECONDS = 5

    def __init__(self, display, data_sources, notifications):
        self._display = display
        self._logger = logging.getLogger('doodledashboard.Dashboard')
        self._data_sources = data_sources
        self._notifications = notifications
        self._update_interval = Dashboard._FIVE_SECONDS

    def set_update_interval(self, interval):
        self._update_interval = interval

    def start(self):
        messages = []
        for notification in itertools.cycle(self._notifications):

            if self._is_at_beginning(notification):
                self._logger.info('At beginning of notification cycle, will poll data sources')
                messages = self._collect_all_messages(self._data_sources)
                self._logger.info('%s messages collected' % len(messages))

            notification.handle_messages(self._display, messages)
            time.sleep(self._update_interval)

    def _is_at_beginning(self, notification):
        return notification is self._notifications[0]

    @staticmethod
    def _collect_all_messages(repositories):
        messages = []
        for repository in repositories:
            messages += repository.get_latest_messages()

        return messages


class Notification:
    def __init__(self, handler):
        self._handler = handler
        self._filter_chain = None

    def set_filter_chain(self, filter_chain):
        self._filter_chain = filter_chain

    def handle_messages(self, display, messages):
        filtered_messages = self._filter_messages(messages)

        self._handler.update(filtered_messages)
        self._handler.draw(display)

    def _filter_messages(self, messages):
        if self._filter_chain:
            return self._filter_chain.filter(messages)
        else:
            return messages

    def __str__(self):
        return "Displays messages using: %s" % str(self._handler)
