import click
import textwrap
from ratelimit import limits, sleep_and_retry
from sketchingdev.image_to_ascii.centre import centre_in_container

from doodledashboard.component import ComponentConfig, DisplayConfig
from doodledashboard.displays.display import Display
from doodledashboard.notifications.outputs import TextNotificationOutput, ImageNotificationOutput


def _contains_all_in_error_message(error, words):
    msg = str(error).lower()

    for word in words:
        if word.lower() not in msg:
            return False

    return True


try:
    from sketchingdev.image_to_ascii.converter import format_image
except ImportError as err:
    if _contains_all_in_error_message(err, ["libopenjp2.so.7", "no such file or directory"]):
        raise ImportError(
            "Your device is missing the dependency 'libopenjp2-7', which is used by the library 'Pillow' to " +
            "allow me to access pixels from the image to draw as ASCII characters. Don't worry though! It should be " +
            "easy enough to install by running 'sudo apt-get install libopenjp2-7'"
        )
    else:
        raise


def _handle_text(size, notification):
    text = notification.text
    width = size[0]
    height = size[1]

    wrapped_lines = textwrap.wrap(text, width)
    cropped = wrapped_lines[:height]

    centred = centre_in_container(cropped, size)

    return "\n".join(centred)


def _handle_image(size, notification):
    return format_image(size, notification.image_path)


class LimitCalls(object):
    def __init__(self, period=10):
        self._limits = limits(calls=1, period=period, raise_on_limit=False)

    def __call__(self, original_func):
        def update_limit_period(*args, **kwargs):
            console = args[0]
            self._limits.period = console.seconds_per_notification
            return self._limits(original_func)(*args, **kwargs)

        return update_limit_period


class ConsoleDisplay(Display):
    """
    Draws a notification to the console every 5 seconds
    """

    _DEFAULT_PERIOD = 5

    _UNSUPPORTED_NOTIFICATION_ERROR = "Notification type '%s' not supported by this display"

    _NOTIFICATIONS = {
        TextNotificationOutput: _handle_text,
        ImageNotificationOutput: _handle_image
    }

    def __init__(self, show_notification_names=False, period=_DEFAULT_PERIOD, size=click.get_terminal_size()):
        super().__init__()
        self._show_notification_names = show_notification_names
        self._seconds_per_notification = period

        if show_notification_names and size[1] > 1:
            self._size = self._reduce_height_by_1(size)
        else:
            self._size = size

    @sleep_and_retry
    @LimitCalls(period=_DEFAULT_PERIOD)
    def draw(self, notification):
        click.clear()
        factory = self._find_factory(notification)

        if self._show_notification_names:
            click.echo(notification.name)

        click.echo(factory(self._size, notification), nl=False)

    def _find_factory(self, notification, default=lambda x, y: ConsoleDisplay._UNSUPPORTED_NOTIFICATION_ERROR % str(y)):
        for factory_type, factory in self._NOTIFICATIONS.items():
            if isinstance(notification, factory_type):
                return factory

        return default

    @staticmethod
    def _reduce_height_by_1(size):
        return size[0], size[1] - 1

    @staticmethod
    def get_supported_notifications():
        return ConsoleDisplay._NOTIFICATIONS.keys()

    @property
    def seconds_per_notification(self):
        return self._seconds_per_notification

    def __str__(self):
        return "Console display"


class ConsoleDisplayConfig(ComponentConfig, DisplayConfig):

    @staticmethod
    def get_id():
        return "console"

    def create(self, options):
        show_notification_names = options.get("show-name-of-notification", False)
        seconds_per_notification = options.get("seconds-per-notifications", ConsoleDisplay._DEFAULT_PERIOD)
        return ConsoleDisplay(show_notification_names, seconds_per_notification)
