import json
import unittest

from click.testing import CliRunner

from doodledashboard.cli import view
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestCliViewDataFeeds(CliTestCase):

    def test_no_source_data_shown_when_no_config_provided(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "datafeeds")

        data = json.loads(result.output)
        self.assertEqual([], data["source-data"], result.output)
        self.assertEqual(0, result.exit_code)

    def test_no_source_data_shown_when_config_empty(self):
        empty_configuration = ""

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", empty_configuration)
            result = self.call_cli(runner, view, "datafeeds config.yml")

        data = json.loads(result.output)
        self.assertEqual([], data["source-data"], result.output)
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
            result = self.call_cli(runner, view, "datafeeds single_config-output.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["source-data"]), "Source data should contain 1 message")
        self.assertEqual("Test 1", data["source-data"][0]["text"], "Text in the message should equal Test 1")
        self.assertEqual(0, result.exit_code)

    def test_multiple_messages_displayed_from_single_feed(self):
        config_with_single_feed_that_outputs_multiple_messages = """
        data-feeds:
          - source: text
            text:
              - Test 1
              - Test 2
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("multiple-output.yml", config_with_single_feed_that_outputs_multiple_messages)
            result = self.call_cli(runner, view, "datafeeds multiple-output.yml")

        data = json.loads(result.output)
        self.assertEqual(2, len(data["source-data"]), "Source data should contain 2 messages")
        self.assertEqual("Test 1", data["source-data"][0]["text"], "Text in the first message should equal Test 1")
        self.assertEqual("Test 2", data["source-data"][1]["text"], "Text in the second message should equal Test 2")
        self.assertEqual(0, result.exit_code)

    def test_multiple_messages_displayed_from_multiple_feeds_together_in_one_array(self):
        config_with_multiple_feed_that_outputs_multiple_messages = """
        data-feeds:
          - source: text
            text:
              - Test 1
              - Test 2
          - source: text
            text:
              - Test 3
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("multiple-output.yml", config_with_multiple_feed_that_outputs_multiple_messages)
            result = self.call_cli(runner, view, "datafeeds multiple-output.yml")

        data = json.loads(result.output)
        self.assertEqual(3, len(data["source-data"]), "Source data should contain 3 messages")
        self.assertEqual("Test 1", data["source-data"][0]["text"], "Text in the first message should equal Test 1")
        self.assertEqual("Test 2", data["source-data"][1]["text"], "Text in the second message should equal Test 2")
        self.assertEqual("Test 3", data["source-data"][2]["text"], "Text in the second message should equal Test 3")
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
