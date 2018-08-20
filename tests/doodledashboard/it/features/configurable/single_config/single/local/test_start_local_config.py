import unittest

from click.testing import CliRunner

from doodledashboard.cli import start
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestCliStartLocalConfig(CliTestCase):

    def test_single_config_with_invalid_display_shows_error(self):
        config_with_invalid_display = """
        display: none
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("invalid_config.yml", config_with_invalid_display)
            result = self.call_cli(runner, start, "invalid_config.yml")

        self.assertIn(
            "Cannot find the display 'none'. Have you run `pip install` for the display you're trying to use?",
            result.output)
        self.assertEqual(1, result.exit_code)

    def test_malformed_config_displays_error(self):
        malformed_display = """
        :
        """

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("malformed_config.yml", malformed_display)
            result = self.call_cli(runner, start, "malformed_config.yml")

        self.assertIn("Error while parsing a block mapping", result.output)
        self.assertEqual(1, result.exit_code)

    def test_default_interval_used_if_none_provided(self):
        config_without_interval = ""

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_without_interval)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("Interval: 15", result.output)
        self.assertEqual(0, result.exit_code)

    def test_notification_with_datafeed_loaded_from_config(self):
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


if __name__ == '__main__':
    unittest.main()
