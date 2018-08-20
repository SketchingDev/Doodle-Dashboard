import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from tests.doodledashboard.it.features.displays.dummy_displays import DummyDisplay
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestCliListDisplays(CliTestCase):

    def test_display_shown_in_list_of_available_displays(self):
        StaticComponentLoader.displays.append(DummyDisplay)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "displays")

        self.assertIn("Available displays:", result.output)
        self.assertIn(" - test-display", result.output)
        self.assertEqual(0, result.exit_code)

    def test_display_shown_in_list_all(self):
        StaticComponentLoader.datafeeds.append(DummyDisplay)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available displays:", result.output)
        self.assertIn(" - test-display", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
