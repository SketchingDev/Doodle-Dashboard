from doodledashboard.configuration.config import ConfigSection

from doodledashboard.updaters.updater import NotificationUpdater


class TextNotificationUpdater(NotificationUpdater):

    def _update(self, notification, message):
        notification.set_text(message.get_text())

    @staticmethod
    def get_config_factory():
        return TextNotificationUpdaterConfig()


class TextNotificationUpdaterConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "name", "text-from-message"

    def create(self, config_section):
        return TextNotificationUpdater()
