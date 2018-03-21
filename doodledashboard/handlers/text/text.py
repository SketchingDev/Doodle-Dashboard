import os
from os import path

from doodledashboard.config import MissingRequiredOptionException
from doodledashboard.handlers.handler import MessageHandler, MessageHandlerConfigCreator


class TextHandler(MessageHandler):
    _FONT_FILENAME = "Noteworthy.ttc"

    def __init__(self, shelve, title):
        MessageHandler.__init__(self, shelve)

        current_dir = self._get_current_directory()
        self._font_full_path = path.join(current_dir, TextHandler._FONT_FILENAME)
        self._title = title

        if self.key_value_store.has_key(self._title):
            self._text = self.key_value_store[self._title]
        else:
            self._text = ""

    def update(self, messages):
        if messages:
            self._text = TextHandler._get_latest(messages).get_text()
            self.key_value_store[self._title] = self._text

    def draw(self, display):
        display.write_text(self._title, 0, 0, 45, self._font_full_path)
        display.write_text(self._text, 0, 20, 45, self._font_full_path)
        display.flush()

    @staticmethod
    def _get_latest(messages):
        return messages[-1]

    @staticmethod
    def _get_current_directory():
        return os.path.dirname(os.path.realpath(__file__))

    def __str__(self):
        return "Text handler for '%s'" % self._title


class TextMessageHandlerConfigCreator(MessageHandlerConfigCreator):
    def __init__(self, key_value_storage):
        MessageHandlerConfigCreator.__init__(self, key_value_storage)

    def create_handler(self, config_section, key_value_store):
        if 'title' not in config_section:
            raise MissingRequiredOptionException('\'title\' must be set in: %s' % str(config_section))

        if not config_section['title']:
            raise MissingRequiredOptionException('\'title\' must have a value in: %s' % str(config_section))

        return TextHandler(key_value_store, str(config_section['title']))

    def creates_for_id(self, filter_id):
        return filter_id == 'text-handler'
