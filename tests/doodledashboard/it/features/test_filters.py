import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from doodledashboard.component import StaticComponentSource, FilterConfig
from doodledashboard.filters.filter import MessageFilter
from tests.doodledashboard.it.support import CliTestCase


class DummyFilter(MessageFilter):

    def filter(self, messages):
        return messages


class DummyFilterConfig(FilterConfig):

    @staticmethod
    def get_id():
        return "test-filter"

    def create(self, options, secret_storage):
        return DummyFilter()


class ListCommand(CliTestCase):

    def test_filter_shown_in_list_of_available_filters(self):
        StaticComponentSource.add(DummyFilterConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "filters")

        self.assertIn("Available filters:", result.output)
        self.assertIn(" - test-filter", result.output)
        self.assertEqual(0, result.exit_code)

    def test_filter_shown_in_list_all(self):
        StaticComponentSource.add(DummyFilterConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available filters:", result.output)
        self.assertIn(" - test-filter", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
