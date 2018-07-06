from abc import ABC, abstractmethod


class NotificationUpdater(ABC):

    def __init__(self):
        self._message_filters = []

    def update(self, notification, message):
        if self._keep_message(message):
            self._update(notification, message)

    @abstractmethod
    def _update(self, notification, message):
        pass

    def add_message_filters(self, filters):
        self._message_filters.extend(filters)

    def _keep_message(self, message):
        for f in self._message_filters:
            if f.filter(message) is False:
                return False

        return True

    @staticmethod
    @abstractmethod
    def get_config_factory():
        return None
