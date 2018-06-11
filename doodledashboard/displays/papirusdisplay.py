from papirus import Papirus, PapirusText, PapirusImage
from doodledashboard.displays.display import CanWriteText, CanDrawImage, Display


class PapirusDisplay(Display, CanDrawImage, CanWriteText):

    def __init__(self):
        self._screen = Papirus()
        self._image = PapirusImage()
        self._text = PapirusText()

    def clear(self):
        self._screen.update()

    def draw_image(self, image_path):
        self._image.write(image_path)

    def write_text(self, text, font_face=None):
        self._text.write(text)

    @staticmethod
    def get_id():
        return "papirus"

    def __str__(self):
        return "Papirus display"
