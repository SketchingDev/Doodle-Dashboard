from doodledashboard.component import FilterConfig, MissingRequiredOptionException, ComponentConfig
from doodledashboard.filters.filter import MessageFilter


class MessageFromSourceFilter(MessageFilter):
    def __init__(self, source_name):
        MessageFilter.__init__(self)
        self._source_name = source_name

    def filter(self, message):
        return message.source_name == self._source_name

    @property
    def source_name(self):
        return self._source_name


class MessageFromSourceFilterConfig(ComponentConfig, FilterConfig):

    @staticmethod
    def get_id():
        return "message-from-source"

    def create(self, options):
        if "source-name" not in options:
            raise MissingRequiredOptionException("Expected 'source-name' option to exist")

        return MessageFromSourceFilter(str(options["source-name"]))
