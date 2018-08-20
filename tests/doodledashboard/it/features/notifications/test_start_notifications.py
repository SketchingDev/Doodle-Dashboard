import unittest

from click.testing import CliRunner

from doodledashboard.cli import start
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestCliStartNotifications(CliTestCase):

    def test_no_notifications_loaded_if_config_empty(self):
        empty_config = ""

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", empty_config)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("0 notifications loaded", result.output)
        self.assertEqual(0, result.exit_code)

    def test_single_notification_displayed(self):
        config_with_single_notification = """
        interval: 0
        data-feeds:
          - source: text
            text:
              - Test Message 1
        notifications:
          - title: Print message
            type: text
            update-with:
              name: text-from-message
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("single_config-notification.yml", config_with_single_notification)
            result = self.call_cli(runner, start, "single_config-notification.yml --once")

        self.assertIn("1 notifications loaded", result.output)
        self.assertIn("Test Message 1", result.output)
        self.assertEqual(0, result.exit_code)

    def test_multiple_notifications_displayed(self):
        config_with_multiple_notifications = """
        interval: 0
        data-feeds:
          - source: text
            text:
              - Test Message 1
              - Test Message 2
              - Test Message 3
        notifications:
          - title: Print message 1
            type: text
            update-with:
              name: text-from-message
              filter-messages:
                - type: message-contains-text
                  text: "1"
          - title: Print message 2
            type: text
            update-with:
              name: text-from-message
              filter-messages:
                - type: message-contains-text
                  text: "2"
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("multiple-notifications.yml", config_with_multiple_notifications)
            result = self.call_cli(runner, start, "multiple-notifications.yml --once")

        self.assertIn("2 notifications loaded", result.output)
        self.assertIn("Test Message 1", result.output)
        self.assertIn("Test Message 2", result.output)
        self.assertNotIn("Test Message 3", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
