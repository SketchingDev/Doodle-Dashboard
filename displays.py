import logging
# from papirus import PapirusText


class Display:
    def __init__(self):
        self.logger = logging.getLogger('raspberry_pi_dashboard.Display')

    def clear(self):
        self.logger.info("Clear display")

    def draw_text(self, text):
        self.logger.info("Draw text: '%s'" % text)

#
# class PapirusDisplay(Display):
#
#     def __init__(self):
#         Display.__init__(self)
#         self._papirus_text = PapirusText()
#
#     def clear(self):
#         self.logger.info("Clear display")
#
#     def draw_text(self, text):
#         self._papirus_text.write(text)
#         self.logger.info("Draw text")