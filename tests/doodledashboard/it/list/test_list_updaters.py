import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from doodledashboard.configuration.config import ConfigSection
from doodledashboard.updaters.updater import NotificationUpdater
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class DummyNotificationUpdater(NotificationUpdater):

    def _update(self, notification, message):
        pass

    @staticmethod
    def get_config_factory():
        return DummyNotificationUpdaterConfig()


class DummyNotificationUpdaterConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "name", "test-notification-updater"

    def create(self, config_section):
        return DummyNotificationUpdater()


class TestCliListNotificationUpdaters(CliTestCase):

    def test_updater_shown_in_list_of_available_updaters(self):
        StaticComponentLoader.notification_updaters.append(DummyNotificationUpdater)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "updaters")

        self.assertIn("Available updaters:", result.output)
        self.assertIn(" - test-notification-updater", result.output)
        self.assertEqual(0, result.exit_code)

    def test_updater_shown_in_list_all(self):
        StaticComponentLoader.notification_updaters.append(DummyNotificationUpdater)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available updaters:", result.output)
        self.assertIn(" - test-notification-updater", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
