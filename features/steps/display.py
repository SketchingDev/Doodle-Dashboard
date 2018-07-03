import click
from behave import given

from doodledashboard.configuration.component_loaders import StaticDisplayLoader
from doodledashboard.display import Display
from doodledashboard.notifications import TextNotification


@given("I load test displays")
def _i_have_the_configuration_x(context):
    StaticDisplayLoader.displays.extend([DisplayWithNoNotificationSupport, DisplayWithNotificationSupport])


class DisplayWithNoNotificationSupport(Display):

    def draw(self, notification):
        if notification.__class__ not in self.get_supported_notifications():
            return

    @staticmethod
    def get_id():
        return "test-display-no-functionality"

    @staticmethod
    def get_supported_notifications():
        return []

    def __str__(self):
        return self.get_id()


class DisplayWithNotificationSupport(Display):

    def draw(self, notification):
        if notification.__class__ not in self.get_supported_notifications():
            return

        click.echo("Displaying %s" % str(notification))

    @staticmethod
    def get_supported_notifications():
        return [TextNotification]

    @staticmethod
    def get_id():
        return "test-display-all-functionality"

    def __str__(self):
        return self.get_id()
