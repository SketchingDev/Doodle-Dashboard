import unittest

import json
from click.testing import CliRunner

from doodledashboard.cli import start, view
from doodledashboard.component import ComponentConfig, NotificationConfig, StaticComponentSource
from doodledashboard.notifications.notification import Notification
from doodledashboard.notifications.outputs import NotificationOutput
from tests.doodledashboard.it.support import CliTestCase


class DummyNotificationOutput(NotificationOutput):
    pass


class DummyNotification(Notification):

    def __init__(self, options):
        super().__init__()

    def create_output(self, messages):
        pass

    def get_output_types(self):
        return [DummyNotificationOutput]


class DummyNotificationConfig(ComponentConfig, NotificationConfig):

    @staticmethod
    def get_id():
        return "test-notification-with-unsupported-output"

    def create(self, options):
        return DummyNotification(options)


class StartCommand(CliTestCase):

    def test_default_display_used_when_no_display_in_config(self):
        config_without_display = """
        dashboard:
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("no_display.yml", config_without_display)
            result = self.call_cli(runner, start, "no_display.yml --once")

        self.assertIn("Display loaded: Console display", result.output)
        self.assertEqual(0, result.exit_code)

    def test_single_config_with_invalid_display_shows_error(self):
        config_with_invalid_display = """
        dashboard:
          display:
            type: non-existent
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("invalid_config.yml", config_with_invalid_display)
            result = self.call_cli(runner, start, "invalid_config.yml")

        self.assertIn(
            "Cannot find the display 'non-existent'. Have you run `pip install` for the display you're trying to use?",
            result.output)
        self.assertEqual(1, result.exit_code)

    def test_malformed_config_displays_error(self):
        malformed_display = """
        :
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("malformed_config.yml", malformed_display)
            result = self.call_cli(runner, start, "malformed_config.yml")

        self.assertIn("Error while parsing a block mapping", result.output)
        self.assertEqual(1, result.exit_code)

    def test_notification_with_datafeed_loaded_from_config(self):
        config_with_single_notification = """
        dashboard:
          display:
            type: console
            options:
              seconds-per-notifications: 0
          data-feeds:
            - type: text
              options:
                text:
                  - Test Message 1
          notifications:
            - name: Print message
              type: text-from-message
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("single_config-notification.yml", config_with_single_notification)
            result = self.call_cli(runner, start, "single_config-notification.yml --once")

        self.assertIn("1 notifications loaded", result.output)
        self.assertIn("Test Message 1", result.output)
        self.assertEqual(0, result.exit_code)

    def test_display_that_does_not_support_notification_output_shows_error(self):
        StaticComponentSource.add(DummyNotificationConfig)
        config_with_unsupported_output = """
        dashboard:
          display:
            type: console
          notifications:
            - name: Notification with unsupported output
              type: test-notification-with-unsupported-output
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config_with_unsupported_output.yml", config_with_unsupported_output)
            result = self.call_cli(runner, start, "config_with_unsupported_output.yml --once")
        self.assertIn("does not support the notification output", result.output)
        self.assertEqual(1, result.exit_code)


class ViewCommand(CliTestCase):

    def test_invalid_display_shows_error(self):
        config_with_invalid_display = """
        dashboard:
          display:
            type: non-existent
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("invalid_config.yml", config_with_invalid_display)
            result = self.call_cli(runner, view, "datafeeds invalid_config.yml")

        self.assertIn(
            "Cannot find the display 'non-existent'. Have you run `pip install` for the display you're trying to use?",
            result.output)
        self.assertEqual(1, result.exit_code)

    def test_malformed_config_displays_error(self):
        malformed_config = """
        :
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("malformed_config.yml", malformed_config)
            result = self.call_cli(runner, view, "datafeeds malformed_config.yml")

        self.assertIn("Error while parsing a block mapping", result.output)
        self.assertEqual(1, result.exit_code)

    def test_notification_with_datafeed_and_filter_loaded_from_config(self):
        config = """
        dashboard:
          data-feeds:
            - type: text
              options:
                text: Test value 1
          notifications:
            - name: Print any message containing 1
              type: text-from-message
              filters:
                - type: message-contains-text
                  options:
                    text: 1
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config)
            result = self.call_cli(runner, view, "notifications config.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["notifications"]), "There should be one notification")
        notification = data["notifications"][0]

        self.assertEqual("Text (name=Print any message containing 1, text=Test value 1)",
                         notification["notification"],
                         "Notification after being passed filtered message")


if __name__ == '__main__':
    unittest.main()
