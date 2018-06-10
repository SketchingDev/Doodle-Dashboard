from abc import ABC, abstractmethod

from doodledashboard.configuration.config import ConfigSection


class CanWriteText(ABC):
    """Mixin that indicates the display can write text"""

    @abstractmethod
    def write_text(self, text):
        pass


class CanDrawImage(ABC):
    """Mixin that indicates the display can draw an image"""
    @abstractmethod
    def draw_image(self, path):
        pass


class CanColourFill(ABC):
    """Mixin that indicates the display can be filled with colour"""

    @abstractmethod
    def fill_colour(self, colour):
        pass


class Display(ABC):
    @abstractmethod
    def clear(self):
        pass


class DisplayConfigSection(ConfigSection):
    def __init__(self):
        ConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "display" in config_section and self.creates_for_id(config_section["display"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")
