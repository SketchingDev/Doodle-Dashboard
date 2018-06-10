from abc import ABC, abstractmethod

from doodledashboard.configuration.config import ConfigSection


class WriteTextMixin(ABC):
    @abstractmethod
    def write_text(self, text):
        pass


class DrawImageMixin(ABC):
    @abstractmethod
    def draw_image(self, path):
        pass


class ColourFillMixin(ABC):
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
