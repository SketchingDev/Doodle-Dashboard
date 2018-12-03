import json
import unittest

from click.testing import CliRunner

from doodledashboard.cli import list, view
from doodledashboard.component import ComponentConfig, DataFeedConfig, StaticComponentSource
from doodledashboard.datafeeds.datafeed import DataFeed
from tests.doodledashboard.it.support import CliTestCase


class DummyFeed(DataFeed):

    def get_latest_messages(self):
        return []


class DummyFeedConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "test-feed"

    def create(self, options):
        return DummyFeed()


class ListCommand(CliTestCase):

    def test_data_feed_shown_in_list_of_available_data_feeds(self):
        StaticComponentSource.add(DummyFeedConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "datafeeds")

        self.assertIn("Available datafeeds:", result.output)
        self.assertIn(" - test-feed", result.output)
        self.assertEqual(0, result.exit_code)

    def test_data_feed_shown_in_list_all(self):
        StaticComponentSource.add(DummyFeedConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available datafeeds:", result.output)
        self.assertIn(" - test-feed", result.output)
        self.assertEqual(0, result.exit_code)


class ViewCommand(CliTestCase):

    def test_no_source_data_shown_when_no_config_provided(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "datafeeds")

        data = json.loads(result.output)
        self.assertEqual([], data["source-data"], result.output)
        self.assertEqual(0, result.exit_code)

    def test_no_source_data_shown_when_config_empty(self):
        empty_configuration = """
        dashboard:
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", empty_configuration)
            result = self.call_cli(runner, view, "datafeeds config.yml")

        data = json.loads(result.output)
        self.assertEqual([], data["source-data"], result.output)
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
            result = self.call_cli(runner, view, "datafeeds single_config-output.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["source-data"]), "Source data should contain 1 message")
        self.assertEqual("Test 1", data["source-data"][0]["text"], "Text in the message should equal Test 1")
        self.assertEqual(0, result.exit_code)

    def test_multiple_messages_displayed_from_single_feed(self):
        config_with_single_feed_that_outputs_multiple_messages = """
        dashboard:
          data-feeds:
            - type: text
              options:
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
        dashboard:
          data-feeds:
            - type: text
              options:
                text:
                  - Test 1
                  - Test 2
            - type: text
              options:
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
