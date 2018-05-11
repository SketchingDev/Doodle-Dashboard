from papirus import Papirus, PapirusComposite

from doodledashboard.displays.display import Display, DisplayConfigCreator


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

    def __str__(self):
        return f"Papirus display {self._screen_size}"


class PapirusDisplayConfigCreator(DisplayConfigCreator):

    _DISPLAYS = {
        "papirus-1.44inch": PapirusDisplay.A_1_44_INCH,
        "papirus-1.9inch": PapirusDisplay.A_1_9_INCH,
        "papirus-2.0inch": PapirusDisplay.A_2_0_INCH,
        "papirus-2.6inch": PapirusDisplay.A_2_6_INCH,
        "papirus-2.7inch": PapirusDisplay.A_2_7_INCH
    }

    def __init__(self):
        DisplayConfigCreator.__init__(self)

    def creates_for_id(self, display_id):
        return display_id in PapirusDisplayConfigCreator._DISPLAYS.keys()

    def create_item(self, config_section):
        size = PapirusDisplayConfigCreator._DISPLAYS.get(config_section["display"])
        return PapirusDisplay(size)
