from abc import ABC, abstractmethod


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
    """Base class that every display must implement"""
    @abstractmethod
    def clear(self):
        pass

    @staticmethod
    @abstractmethod
    def get_id():
        pass
