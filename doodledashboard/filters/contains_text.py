from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.filters.filter import TextEntityFilter, FilterConfigSection


class ContainsTextFilter(TextEntityFilter):
    def __init__(self, text):
        TextEntityFilter.__init__(self)
        self._text = text

    def filter(self, text_entity):
        return self._text in text_entity.get_text()

    def remove_text(self, text_entity):
        return text_entity.get_text() \
            .replace(self._text, "") \
            .strip()

    def get_text(self):
        return self._text


class ContainsTextFilterSection(FilterConfigSection):
    def __init__(self):
        FilterConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "message-contains-text"

    def create_item(self, config_section):
        if "text" not in config_section:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return ContainsTextFilter(str(config_section["text"]))
