from sketchingdev.displays import Display, CanWriteText, CanDrawImage, CanColourFill


class RecordDisplay(Display, CanWriteText, CanDrawImage, CanColourFill):
    """
    Records the interaction with the display
    """

    def __init__(self):
        self.calls = []

    def clear(self):
        self.calls.append("Clear display")

    def write_text(self, text):
        self.calls.append("Write text: '%s'" % text)

    def draw_image(self, image_path):
        self.calls.append("Draw image: '%s'" % image_path)

    def fill_colour(self, colour):
        self.calls.append("Fill display with colour: '%s'" % colour)

    def get_calls(self):
        return self.calls

    @staticmethod
    def get_id():
        return "record"

    def __str__(self):
        return "Record display"
