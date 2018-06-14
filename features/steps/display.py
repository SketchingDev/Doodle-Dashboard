import click
from behave import given
from sketchingdev.displays import Display, CanWriteText, CanDrawImage, CanColourFill

from doodledashboard.configuration.component_loaders import StaticDisplayLoader


@given("I load test displays")
def _i_have_the_configuration_x(context):
    StaticDisplayLoader.displays.extend([DisplayWithNoMixins, DisplayWithAllMixins])


class DisplayWithNoMixins(Display):
    def clear(self):
        pass

    @staticmethod
    def get_id():
        return "test-display-no-functionality"

    def __str__(self):
        return self.get_id()


class DisplayWithAllMixins(Display, CanWriteText, CanDrawImage, CanColourFill):
    """
    Records the interaction with the display
    """

    def __init__(self):
        self.calls = []

    def clear(self):
        click.echo("Clear display")

    def write_text(self, text):
        click.echo("Write text: '%s'" % text)

    def draw_image(self, image_path):
        click.echo("Draw image: '%s'" % image_path)

    def fill_colour(self, colour):
        click.echo("Fill display with colour: '%s'" % colour)

    @staticmethod
    def get_id():
        return "test-display-all-functionality"

    def __str__(self):
        return self.get_id()
