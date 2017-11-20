from papirus import Papirus, PapirusComposite

from doodledashboard.lucas.displays.display import Display


class PapirusDisplay(Display):

    _SUPPORTED_SIZE = (264, 176)

    def __init__(self):
        Display.__init__(self)
        self._screen = Papirus()
        self._screenComposite = PapirusComposite(False)

    def clear(self):
        self._screen.update()

    def draw_image(self, image_path, x, y, size):
        self._screenComposite.AddImg(image_path, x, y, size)

    def write_text(self, text, x, y, font_size=10, font_face=None):
        self._screenComposite.AddText(str(text), x, y, font_size, fontPath=font_face)

    def flush(self):
        self._screenComposite.WriteAll()

    def get_size(self):
        return PapirusDisplay._SUPPORTED_SIZE



