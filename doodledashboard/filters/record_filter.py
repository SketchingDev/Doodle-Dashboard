from doodledashboard.filters.filter import MessageFilter


class RecordFilter(MessageFilter):
    def __init__(self):
        MessageFilter.__init__(self)
        self._messages = []

    def filter(self, message):
        self._messages.append(message)
        return True

    def get_messages(self):
        return self._messages

    @staticmethod
    def get_config_factory():
        return None
