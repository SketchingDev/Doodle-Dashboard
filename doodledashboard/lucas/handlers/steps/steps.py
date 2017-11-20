import os
from os import path

from doodledashboard.lucas.handlers.handler import MessageHandler


class StepsHandler(MessageHandler):
    _SAVED_VALUE_KEY = "STEPS_HANDLER_LAST_KNOWN_STEPS"
    _BACKGROUND_FILENAME = "background.bmp"
    _FONT_FILENAME = "Noteworthy.ttc"

    def __init__(self, shelve):
        MessageHandler.__init__(self, shelve)

        current_dir = self._get_current_directory()
        self._background_full_path = path.join(current_dir, StepsHandler._BACKGROUND_FILENAME)
        self._font_full_path = path.join(current_dir, StepsHandler._FONT_FILENAME)

    def get_tag(self):
        return '#steps'

    def draw(self, display, messages):
        steps = self._extract_latest_steps(messages, '')

        if steps is '':
            if self.shelve.has_key(StepsHandler._SAVED_VALUE_KEY):
                steps = self.shelve[StepsHandler._SAVED_VALUE_KEY]
            else:
                steps = '0'
        else:
            self.shelve[StepsHandler._SAVED_VALUE_KEY] = steps

        display.draw_image(self._background_full_path, 0, 0, display.get_size())
        display.write_text("Steps so far", 70, 50, 40, self._font_full_path)
        display.write_text(steps, 100, 105, 45, self._font_full_path)
        display.flush()

    def _get_current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def _extract_latest_steps(self, messages, default):
        if not messages:
            return default
        else:
            text = messages[-1].get_text()
            return text.replace(self.get_tag(), '').strip()
