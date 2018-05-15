import click

from doodledashboard.displays.display import DisplayConfigSection, Display


class ConsoleDisplay(Display):
    def __init__(self):
        Display.__init__(self)

    def clear(self):
        click.clear()

    def write_text(self, text, font_face=None):
        click.echo(text)

    def draw_image(self, image_path):
        click.echo("One day I'll draw an ASCII version of %s" % image_path)

    def fill_colour(self, colour):
        click.secho(colour, fg=colour)

    def _get_size(self):
        return click.get_terminal_size()

    def __str__(self):
        return "Console display"


class ConsoleDisplayConfigCreator(DisplayConfigSection):
    def __init__(self):
        DisplayConfigSection.__init__(self)

    def creates_for_id(self, display_id):
        return display_id == "console"

    def create_item(self, config_section):
        return ConsoleDisplay()
