import re

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.configuration.config import Creator


class MessageFilter:
    def __init__(self):
        self._successor = None

    def add(self, successor):
        if not self._successor:
            self._successor = successor
        else:
            self._successor.add(successor)

    def do_filter(self, messages):
        return messages

    def filter(self, messages):
        filtered_messages = self.do_filter(messages)

        if self._successor:
            return self._successor.filter(filtered_messages)
        else:
            return filtered_messages


class FilterConfigCreator(Creator):
    def __init__(self):
        Creator.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "type" in config_section and self.creates_for_id(config_section["type"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")


class MessageContainsTextFilter(MessageFilter):
    def __init__(self, text):
        MessageFilter.__init__(self)
        self._text = text

    def do_filter(self, messages):
        return [m for m in messages if self._text in m.get_text()]

    def remove_text(self, message):
        return message.get_text() \
            .replace(self._text, "") \
            .strip()

    def get_text(self):
        return self._text


class MessageContainsTextFilterCreator(FilterConfigCreator):
    def __init__(self):
        FilterConfigCreator.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "message-contains-text"

    def create_item(self, config_section):
        if "text" not in config_section:
            raise MissingRequiredOptionException("Expected 'text' option to exist")

        return MessageContainsTextFilter(str(config_section["text"]))


class MessageMatchesRegexFilter(MessageFilter):
    def __init__(self, regex):
        MessageFilter.__init__(self)
        self._regex = re.compile(regex, re.IGNORECASE)

    def do_filter(self, messages):
        return [m for m in messages if self._regex.search(m.get_text())]

    def get_pattern(self):
        return self._regex.pattern


class MessageMatchesRegexTextFilterCreator(FilterConfigCreator):
    def __init__(self):
        FilterConfigCreator.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "message-matches-regex"

    def create_item(self, config_section):
        if "pattern" not in config_section:
            raise MissingRequiredOptionException("Expected 'pattern' option to exist")

        return MessageMatchesRegexFilter(str(config_section["pattern"]))