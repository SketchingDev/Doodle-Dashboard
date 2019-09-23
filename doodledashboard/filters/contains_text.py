from doodledashboard.component import FilterCreator, MissingRequiredOptionException
from doodledashboard.filters.filter import MessageFilter


class ContainsTextFilter(MessageFilter):
    def __init__(self, text):
        MessageFilter.__init__(self)
        self._text = text

    def filter(self, message):
        return self._text in message.text

    def remove_text(self, text_entity):
        return text_entity.text \
            .replace(self._text, "") \
            .strip()

    @property
    def text(self):
        return self._text


class ContainsTextFilterCreator(FilterCreator):

    @staticmethod
    def get_id():
        return "message-contains-text"

    def create(self, options, secret_store):
        if "text" not in options:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return ContainsTextFilter(str(options["text"]))
