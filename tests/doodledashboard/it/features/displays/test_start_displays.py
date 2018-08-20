import unittest

from click.testing import CliRunner

from doodledashboard.cli import start
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from tests.doodledashboard.it.features.displays.dummy_displays import DummyDisplay
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestCliListDisplays(CliTestCase):

    def test_display_is_loaded_from_config(self):
        config_with_dummy_display = """
        display: test-display
        """

        StaticComponentLoader.displays.append(DummyDisplay)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_with_dummy_display)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("Display loaded: dummy display", result.output)
        self.assertEqual(0, result.exit_code)

    def test_display_is_provided_with_notification(self):
        config_with_single_notification = """
        interval: 0
        display: test-display
        data-feeds:
          - source: text
            text: Test Message 1
        notifications:
          - title: Print message
            type: text
            update-with:
              name: text-from-message
        """

        StaticComponentLoader.displays.append(DummyDisplay)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_with_single_notification)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("Draw notification (Text notification (title=Print message, text=Test Message 1))", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
