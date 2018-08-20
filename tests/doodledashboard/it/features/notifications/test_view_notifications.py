import json
import unittest

from click.testing import CliRunner

from doodledashboard.cli import view
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestCliViewNotifications(CliTestCase):
    config_with_notification_for_any_message_containing_2 = """
    data-feeds:
      - source: text
        text: Test value 1
      - source: text
        text: Test value 2
    notifications:
      - title: Print any message containing 2
        type: text
        update-with:
          name: text-from-message
          filter-messages:
            - type: message-contains-text
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
        empty_configuration = ""

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
        data-feeds:
          - source: text
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
                         "Messages filtered by notification updaters filters are shown")

    def test_updates_to_a_notification_are_shown(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.config_with_notification_for_any_message_containing_2)
            result = self.call_cli(runner, view, "notifications config.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["notifications"]), "There should be one notification")
        notification = data["notifications"][0]

        self.assertEqual("Text notification (title=Print any message containing 2, text=)",
                         notification["notification-before"],
                         "Notification before being passed filtered message")
        self.assertEqual("Text notification (title=Print any message containing 2, text=Test value 2)",
                         notification["notification-after"],
                         "Notification after being passed filtered message")


if __name__ == '__main__':
    unittest.main()
