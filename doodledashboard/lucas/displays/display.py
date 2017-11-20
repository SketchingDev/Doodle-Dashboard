import logging


class Display:
    def __init__(self):
        pass

    def clear(self):
        raise NotImplementedError('Implement this method')

    def write_text(self, text, x, y, font_size=10, font_face=None):
        raise NotImplementedError('Implement this method')

    def draw_image(self, image_path, x, y, size):
        raise NotImplementedError('Implement this method')

    def flush(self):
        raise NotImplementedError('Implement this method')

    def get_size(self):
        raise NotImplementedError('Implement this method')


class LoggingDisplay(Display):
    def __init__(self):
        Display.__init__(self)
        self._logger = logging.getLogger('raspberry_pi_dashboard.LoggingDisplay')

    def clear(self):
        pass
        # self._logger.info("Clear display")

    def write_text(self, text, x, y, font_size=10, font_face=None):
        self._logger.info("Write text: '%s'" % text)

    def draw_image(self, image_path, x, y, size):
        self._logger.info("Draw image: %s" % image_path)

    def flush(self):
        pass
        # self._logger.info("Flush called")

    def get_size(self):
        # self._logger.info("Display size requested")
        return (0, 0)
