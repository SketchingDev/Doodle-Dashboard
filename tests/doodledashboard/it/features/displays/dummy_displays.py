import click

from doodledashboard.configuration.config import ConfigSection
from doodledashboard.display import Display
from doodledashboard.notifications import TextNotification


class DummyDisplay(Display):

    def draw(self, notification):
        click.echo("Draw notification (%s)" % str(notification))

    @staticmethod
    def get_supported_notifications():
        return [TextNotification]

    @staticmethod
    def get_config_factory():
        return DummyDisplayConfig()

    def __str__(self):
        return "dummy display"


class DummyDisplayConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "display", "test-display"

    def create(self, config_section):
        return DummyDisplay()
