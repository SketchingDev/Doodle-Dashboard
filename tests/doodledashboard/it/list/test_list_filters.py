import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from doodledashboard.configuration.config import ConfigSection
from doodledashboard.filters.filter import MessageFilter
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class DummyFilter(MessageFilter):

    def filter(self, message):
        return message

    @staticmethod
    def get_config_factory():
        return DummyFilterConfig()


class DummyFilterConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "type", "test-filter"

    def create(self, config_section):
        return DummyFilter()


class TestCliListFilters(CliTestCase):

    def test_filter_shown_in_list_of_available_filters(self):
        StaticComponentLoader.filters.append(DummyFilter)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "filters")

        self.assertIn("Available filters:", result.output)
        self.assertIn(" - test-filter", result.output)
        self.assertEqual(0, result.exit_code)

    def test_filter_shown_in_list_all(self):
        StaticComponentLoader.datafeeds.append(DummyFilter)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available filters:", result.output)
        self.assertIn(" - test-filter", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
