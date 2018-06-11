import click

from doodledashboard.displays.display import CanWriteText, CanDrawImage, Display


class ConsoleDisplay(Display, CanWriteText, CanDrawImage):

    @staticmethod
    def get_id():
        return "console"

    def clear(self):
        click.clear()

    def write_text(self, text):
        click.echo(text)

    def draw_image(self, image_path):
        click.echo("One day I'll draw an ASCII version of %s" % image_path)

    def _get_size(self):
        return click.get_terminal_size()

    def __str__(self):
        return "Console display"
