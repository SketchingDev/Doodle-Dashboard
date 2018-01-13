from papirus import Papirus, PapirusComposite

from doodledashboard.displays.display import Display


class PapirusDisplay(Display):

    A_1_44_INCH = (128, 90)
    A_1_9_INCH = (144, 128)
    A_2_0_INCH = (200, 96)
    A_2_6_INCH = (232, 128)
    A_2_7_INCH = (264, 176)

    def __init__(self, size):
        Display.__init__(self)
        self._screen = Papirus()
        self._screen_composite = PapirusComposite(False)
        self._screen_size = size

    def clear(self):
        self._screen.update()

    def draw_image(self, image_path, x, y, size):
        self._screen_composite.AddImg(image_path, x, y, size)

    def write_text(self, text, x, y, font_size=10, font_face=None):
        self._screen_composite.AddText(text, x, y, font_size, fontPath=font_face)

    def flush(self):
        self._screen_composite.WriteAll()
        self._screen_composite = PapirusComposite(False)

    def get_size(self):
        return self._screen_size



