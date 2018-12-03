import unittest

import json
from click.testing import CliRunner

from doodledashboard.cli import list, view, start
from doodledashboard.component import StaticComponentSource, ComponentConfig, NotificationConfig
from doodledashboard.notifications.outputs import TextNotificationOutput
from doodledashboard.notifications.notification import Notification
from tests.doodledashboard.it.support import CliTestCase


class DummyNotification(Notification):

    def __init__(self, options):
        super().__init__()
        self._test_option = options["test-option"]

    def create_output(self, messages):
        return TextNotificationOutput(self._test_option)

    def get_output_types(self):
        return [TextNotificationOutput]


class DummyNotificationConfig(ComponentConfig, NotificationConfig):

    @staticmethod
    def get_id():
        return "test-notification-1"

    def create(self, options):
        return DummyNotification(options)


class ListCommand(CliTestCase):

    def test_notification_shown_in_list_of_available_notifications(self):
        StaticComponentSource.add(DummyNotificationConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "notifications")

        self.assertIn("Available notifications:", result.output)
        self.assertIn(" - test-notification-1", result.output)
        self.assertEqual(0, result.exit_code)

    def test_notification_shown_in_list_all(self):
        StaticComponentSource.add(DummyNotificationConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available notifications:", result.output)
        self.assertIn(" - test-notification-1", result.output)
        self.assertEqual(0, result.exit_code)


class StartCommand(CliTestCase):

    def test_no_notifications_loaded_if_config_empty(self):
        empty_config = """
        dashboard:
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", empty_config)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("0 notifications loaded", result.output)
        self.assertEqual(0, result.exit_code)

    def test_single_notification_displayed(self):
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

    def test_options_passed_to_notification(self):
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
            - name: Test access to options
              type: test-notification-1
              options:
                test-option: Value from options
        """

        StaticComponentSource.add(DummyNotificationConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("single_config-notification.yml", config_with_single_notification)
            result = self.call_cli(runner, start, "single_config-notification.yml --once")

        self.assertIn("1 notifications loaded", result.output)
        self.assertIn("Value from options", result.output)
        self.assertEqual(0, result.exit_code)

    def test_multiple_notifications_displayed(self):
        config_with_multiple_notifications = """
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
                  - Test Message 2
                  - Test Message 3
          notifications:
            - name: Print message 1
              type: text-from-message
              filters:
                - type: message-contains-text
                  options:
                    text: "1"
            - name: Print message 2
              type: text-from-message
              filters:
                - type: message-contains-text
                  options:
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


class ViewCommand(CliTestCase):
    config_with_notification_for_any_message_containing_2 = """
    dashboard:
      data-feeds:
        - type: text
          options:
            text: Test value 1
        - type: text
          options:
            text: Test value 2
      notifications:
        - name: Print any message containing 2
          type: text-from-message
          filters:
            - type: message-contains-text
              options:
                text: 2
    """

    def test_no_source_data_or_notifications_shown_when_no_config_provided(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "notifications")

        data = json.loads(result.output)
        self.assertEqual([], data["source-data"], result.output)
        self.assertEqual([], data["notifications"], result.output)
        self.assertEqual(0, result.exit_code)

    def test_no_source_data_or_notifications_shown_when_config_empty(self):
        empty_configuration = """
        dashboard:
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", empty_configuration)
            result = self.call_cli(runner, view, "notifications config.yml")

        data = json.loads(result.output)
        self.assertEqual([], data["source-data"], result.output)
        self.assertEqual([], data["notifications"], result.output)
        self.assertEqual(0, result.exit_code)

    def test_single_message_displayed_from_single_feed(self):
        config_with_single_feed_that_outputs_single_message = """
        dashboard:
          data-feeds:
            - type: text
              options:
                text: Test 1
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("single_config-output.yml", config_with_single_feed_that_outputs_single_message)
            result = self.call_cli(runner, view, "notifications single_config-output.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["source-data"]), "Source data should contain 1 message")
        self.assertEqual("Test 1", data["source-data"][0]["text"], "Text in the message should equal Test 1")
        self.assertEqual(0, result.exit_code)

    def test_messages_filtered_by_a_notifications_updaters_filters_are_displayed(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.config_with_notification_for_any_message_containing_2)
            result = self.call_cli(runner, view, "notifications config.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["notifications"]), "There should be one notification")
        notification = data["notifications"][0]

        self.assertEqual(1, len(notification["filtered-messages"]),
                         "Notification updater should have filtered 1 message for the notification")
        self.assertEqual("Test value 2", notification["filtered-messages"][0]["text"],
                         "Messages filtered by notification filters are shown")

    def test_updates_to_a_notification_are_shown(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.config_with_notification_for_any_message_containing_2)
            result = self.call_cli(runner, view, "notifications config.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["notifications"]), "There should be one notification")
        notification = data["notifications"][0]

        self.assertEqual("Text (name=Print any message containing 2, text=Test value 2)",
                         notification["notification"],
                         "Notification after being passed filtered message")


if __name__ == '__main__':
    unittest.main()
