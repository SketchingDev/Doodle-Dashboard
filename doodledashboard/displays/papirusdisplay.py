from papirus import Papirus, PapirusText, PapirusImage
from doodledashboard.displays.display import DisplayConfigSection, CanWriteText, CanDrawImage, Display


class PapirusDisplay(Display, CanDrawImage, CanWriteText):
    A_1_44_INCH = (128, 90)
    A_1_9_INCH = (144, 128)
    A_2_0_INCH = (200, 96)
    A_2_6_INCH = (232, 128)
    A_2_7_INCH = (264, 176)

    def __init__(self, size):
        self._screen = Papirus()
        self._image = PapirusImage()
        self._text = PapirusText()
        self._screen_size = size

    def clear(self):
        self._screen.update()

    def draw_image(self, image_path):
        self._image.write(image_path)

    def write_text(self, text, font_face=None):
        self._text.write(text)

    def get_size(self):
        return self._screen_size

    def __str__(self):
        return "Papirus display %sx%s" % (self._screen_size[0], self._screen_size[1])


class PapirusDisplayConfigCreator(DisplayConfigSection):
    _DISPLAYS = {
        "papirus-1.44inch": PapirusDisplay.A_1_44_INCH,
        "papirus-1.9inch": PapirusDisplay.A_1_9_INCH,
        "papirus-2.0inch": PapirusDisplay.A_2_0_INCH,
        "papirus-2.6inch": PapirusDisplay.A_2_6_INCH,
        "papirus-2.7inch": PapirusDisplay.A_2_7_INCH
    }

    def __init__(self):
        DisplayConfigSection.__init__(self)

    def creates_for_id(self, display_id):
        return display_id in PapirusDisplayConfigCreator._DISPLAYS.keys()

    def create_item(self, config_section):
        size = PapirusDisplayConfigCreator._DISPLAYS.get(config_section["display"])
        return PapirusDisplay(size)
