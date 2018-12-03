from doodledashboard.component import ComponentConfig, NotificationConfig
from doodledashboard.notifications.outputs import TextNotificationOutput

from doodledashboard.notifications.notification import Notification


class TextInMessage(Notification):
    """Creates a notification containing the text of the last message"""

    def create_output(self, messages):
        return TextNotificationOutput(messages[-1].text) if messages else None

    def get_output_types(self):
        return [TextNotificationOutput]

    def __str__(self):
        return "Text In Message (name=%s)" % self.name


class TextInMessageConfig(ComponentConfig, NotificationConfig):

    @staticmethod
    def get_id():
        return "text-from-message"

    def create(self, options):
        return TextInMessage()
