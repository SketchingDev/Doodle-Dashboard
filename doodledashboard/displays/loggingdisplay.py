from doodledashboard.displays.display import DisplayConfigCreator, Display
import logging


class LoggingDisplay(Display):
    def __init__(self):
        Display.__init__(self)
        self._logger = logging.getLogger('doodle_dashboard.LoggingDisplay')

    def clear(self):
        self._logger.info("Clear display")

    def write_text(self, text, x, y, font_size=10, font_face=None):
        self._logger.info("Write text: '%s'" % text)

    def draw_image(self, image_path, x, y, size):
        self._logger.info("Draw image: %s" % image_path)

    def flush(self):
        self._logger.info("Flush called")

    def get_size(self):
        self._logger.info("Display size requested")
        return 0, 0

    def __str__(self):
        return "Logging display"


class LoggingDisplayConfigCreator(DisplayConfigCreator):
    def __init__(self):
        DisplayConfigCreator.__init__(self)

    def creates_for_id(self, display_id):
        return display_id == 'logging'

    def create_item(self, config_section):
        return LoggingDisplay()
