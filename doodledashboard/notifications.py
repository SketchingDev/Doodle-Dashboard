from abc import ABC, abstractmethod

from doodledashboard.configuration.config import ConfigSection


class Notification(ABC):
    def __init__(self):
        self._updater = None
        self._title = None

    def get_updater(self):
        return self._updater

    def set_updater(self, updater):
        self._updater = updater

    def set_title(self, title):
        self._title = title

    def get_title(self):
        return self._title

    def update(self, message):
        if self._updater:
            self._updater.update(self, message)

    @staticmethod
    @abstractmethod
    def get_config_factory():
        return None


class TextNotification(Notification):

    def __init__(self):
        super().__init__()
        self._image_path = None
        self._text = ""

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def __str__(self):
        return "Text notification (title=%s, text=%s)" % (self.get_title(), self.get_text())

    @staticmethod
    def get_config_factory():
        return TextNotificationConfig()


class TextNotificationConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "text"

    def create(self, config_section):
        notification = TextNotification()

        if "title" in config_section:
            notification.set_title(config_section["title"])

        return notification


class ImageNotification(Notification):
    def __init__(self):
        super().__init__()
        self._image_path = None

    def set_image_path(self, path):
        self._image_path = path

    def get_image_path(self):
        return self._image_path

    def __str__(self):
        return "Image notification (title=%s, image=%s)" % (self.get_title(), self.get_image_path())

    @staticmethod
    def get_config_factory():
        return ImageNotificationConfig()


class ImageNotificationConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "image"

    def create(self, config_section):
        notification = ImageNotification()

        if "title" in config_section:
            notification.set_title(config_section["title"])

        if "path" in config_section:
            notification.set_image_path(config_section["path"])

        return notification


class ImageWithTextNotification(Notification):
    def __init__(self):
        super().__init__()
        self._image_path = None
        self._text = ""

    def set_image_path(self, path):
        self._image_path = path

    def get_image_path(self):
        return self._image_path

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def __str__(self):
        return "Image with text notification (title=%s, image=%s, text=%s)" % \
               (self.get_title(), self.get_image_path(), self.get_text())

    @staticmethod
    def get_config_factory():
        return ImageWithTextNotificationConfig()


class ImageWithTextNotificationConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "image-with-text"

    def create(self, config_section):
        notification = ImageWithTextNotification()

        if "title" in config_section:
            notification.set_title(config_section["title"])

        if "image" in config_section:
            notification.set_image_path(config_section["image"])

        if "text" in config_section:
            notification.set_text(config_section["text"])

        return notification


class ColourNotification(Notification):

    def __init__(self):
        super().__init__()
        self._colour = "#000000"

    def set_colour(self, colour):
        self._colour = colour

    def get_colour(self):
        return self._colour

    def __str__(self):
        return "Colour notification (title=%s, colour=%s)" % (self.get_title(), self.get_colour())

    @staticmethod
    def get_config_factory():
        return ColourNotificationConfig()


class ColourNotificationConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "colour"

    def create(self, config_section):
        notification = ColourNotification()

        if "title" in config_section:
            notification.set_title(config_section["title"])

        if "hex" in config_section:
            notification.set_colour(config_section["hex"])

        return notification
