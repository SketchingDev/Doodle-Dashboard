import click

from doodledashboard.displays.display import DisplayConfigSection, WriteTextMixin, DrawImageMixin, ClearMixin, \
    ColourFillMixin, Display


class ConsoleDisplay(Display, ClearMixin, WriteTextMixin, DrawImageMixin, ColourFillMixin):

    def fill_colour(self, colour):
        pass

    def clear(self):
        click.clear()

    def write_text(self, text):
        click.echo(text)

    def draw_image(self, image_path):
        click.echo("One day I'll draw an ASCII version of %s" % image_path)

    def _get_size(self):
        return click.get_terminal_size()

    # @property
    # def get_display_id(self):
    #     return "console"

    def __str__(self):
        return "Console display"


class ConsoleDisplayConfigCreator(DisplayConfigSection):
    def __init__(self):
        DisplayConfigSection.__init__(self)

    def creates_for_id(self, display_id):
        return display_id == "console"

    def create_item(self, config_section):
        return ConsoleDisplay()
