import unittest

import click
from click.testing import CliRunner

from doodledashboard.cli import list, start
from doodledashboard.component import DisplayConfig
from doodledashboard.component import StaticComponentSource
from doodledashboard.displays.display import Display
from doodledashboard.notifications.outputs import TextNotificationOutput
from tests.doodledashboard.it.support import CliTestCase


class DummyDisplay(Display):

    def draw(self, notification):
        click.echo("Draw notification (%s)" % str(notification))

    @staticmethod
    def get_supported_notifications():
        return [TextNotificationOutput]

    def __str__(self):
        return "dummy display"


class DummyDisplayConfig(DisplayConfig):

    @staticmethod
    def get_id():
        return "test-display"

    def create(self, options, secret_storage):
        return DummyDisplay()


class ListCommand(CliTestCase):

    def test_display_shown_in_list_of_available_displays(self):
        StaticComponentSource.add(DummyDisplayConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "displays")

        self.assertIn("Available displays:", result.output)
        self.assertIn(" - test-display", result.output)
        self.assertEqual(0, result.exit_code)

    def test_display_shown_in_list_all(self):
        StaticComponentSource.add(DummyDisplayConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "all")

        self.assertIn("Available displays:", result.output)
        self.assertIn(" - test-display", result.output)
        self.assertEqual(0, result.exit_code)


class StartCommand(CliTestCase):

    def test_display_is_loaded_from_config(self):
        config_with_dummy_display = """
        dashboard:
          display:
            type: test-display
        """

        StaticComponentSource.add(DummyDisplayConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_with_dummy_display)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("Display loaded: dummy display", result.output)
        self.assertEqual(0, result.exit_code)

    def test_display_is_provided_with_notification(self):
        config_with_single_notification = """
        dashboard:
          display:
            type: test-display
          data-feeds:
            - type: text
              options:
                text: Test Message 1
          notifications:
            - name: Print message
              type: text-from-message
        """

        StaticComponentSource.add(DummyDisplayConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_with_single_notification)
            result = self.call_cli(runner, start, "config.yml --once")

        self.assertIn("Draw notification (Text (name=Print message, text=Test Message 1))", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
