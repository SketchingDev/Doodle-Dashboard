import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from doodledashboard.configuration.config import ConfigSection
from doodledashboard.notifications import Notification
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class DummyNotification(Notification):

    @staticmethod
    def get_config_factory():
        return DummyNotificationConfig()


class DummyNotificationConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "test-notification"

    def create(self, config_section):
        return DummyNotification()


class TestCliListNotifications(CliTestCase):

    def test_notification_shown_in_list_of_available_notifications(self):
        StaticComponentLoader.notifications.append(DummyNotification)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "notifications")

        self.assertIn("Available notifications:", result.output)
        self.assertIn(" - test-notification", result.output)
        self.assertEqual(0, result.exit_code)

    def test_notification_shown_in_list_all(self):
        StaticComponentLoader.notifications.append(DummyNotification)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available notifications:", result.output)
        self.assertIn(" - test-notification", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
