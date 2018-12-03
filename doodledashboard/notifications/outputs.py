from abc import ABC


class NotificationOutput(ABC):
    """ Base class that represents a notification that can be displayed.
    All notifications at very least must have the ability to get a name,
    which the displays can decide whether to show.
    """

    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class TextNotificationOutput(NotificationOutput):

    def __init__(self, text):
        super().__init__()
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def __str__(self):
        return "Text (name=%s, text=%s)" % (self.name, self.text)


class ImageNotificationOutput(NotificationOutput):
    def __init__(self, image_path=None):
        super().__init__()
        self._image_path = image_path

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, path):
        self._image_path = path

    def __str__(self):
        return "Image (name=%s, image=%s)" % (self.name, self.image_path)


class ImageWithTextNotificationOutput(NotificationOutput):
    def __init__(self):
        super().__init__()
        self._image_path = None
        self._text = ""

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, path):
        self._image_path = path

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def __str__(self):
        return "Image with text (name=%s, image=%s, text=%s)" % \
               (self.name, self.image_path, self.text)


class ColourNotificationOutput(NotificationOutput):

    def __init__(self):
        super().__init__()
        self._colour = "#000000"

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        self._colour = colour

    def __str__(self):
        return "Colour (name=%s, colour=%s)" % (self.name, self.get_colour())
