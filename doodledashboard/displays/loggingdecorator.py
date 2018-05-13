import logging

from doodledashboard.displays.display import Display


class LoggingDisplayDecorator(Display):
    def __init__(self, display):
        Display.__init__(self)
        self._logger = logging.getLogger("doodledashboard")
        self._display = display

    def fill_colour(self, colour):
        self._logger.info("Fill with %s" % colour)
        self._display.fill_colour(colour)

    def clear(self):
        self._logger.info("Clear display")
        self._display.clear()

    def write_text(self, text, font_face=None):
        self._logger.info("Write text: '%s'" % text)
        self._display.write_text(text, font_face)

    def draw_image(self, image_path):
        self._logger.info("Draw image: %s" % image_path)
        self._display.draw_image(image_path)

    def __str__(self):
        return self._display.__str__()
