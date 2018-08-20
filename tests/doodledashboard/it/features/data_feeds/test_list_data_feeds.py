import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from doodledashboard.configuration.config import ConfigSection
from doodledashboard.datafeeds.datafeed import DataFeed
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class DummyFeed(DataFeed):

    def get_latest_messages(self):
        return []

    @staticmethod
    def get_config_factory():
        return DummyFeedConfig()


class DummyFeedConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "source", "test-feed"

    def create(self, config_section):
        return DummyFeed()


class TestCliListDataFeeds(CliTestCase):

    def test_data_feed_shown_in_list_of_available_data_feeds(self):
        StaticComponentLoader.datafeeds.append(DummyFeed)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "datafeeds")

        self.assertIn("Available datafeeds:", result.output)
        self.assertIn(" - test-feed", result.output)
        self.assertEqual(0, result.exit_code)

    def test_data_feed_shown_in_list_all(self):
        StaticComponentLoader.datafeeds.append(DummyFeed)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available datafeeds:", result.output)
        self.assertIn(" - test-feed", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
