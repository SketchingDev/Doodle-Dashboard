from doodledashboard.component import NotificationCreator
from doodledashboard.notifications.notification import Notification
from doodledashboard.notifications.outputs import TextNotificationOutput


class TextInMessage(Notification):
    """Creates a notification containing the text of the last message"""

    def create_output(self, messages):
        return TextNotificationOutput(messages[-1].text) if messages else None

    def get_output_types(self):
        return [TextNotificationOutput]

    def __str__(self):
        return "Text In Message (name=%s)" % self.name


class TextInMessageCreator(NotificationCreator):

    @staticmethod
    def get_id():
        return "text-from-message"

    def create(self, options, secret_store):
        return TextInMessage()
