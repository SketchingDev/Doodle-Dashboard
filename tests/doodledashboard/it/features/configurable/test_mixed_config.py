import unittest

import pytest
from click.testing import CliRunner
from pytest_localserver import http

from doodledashboard.cli import start
from doodledashboard.component import StaticComponentSource, ComponentConfig, DisplayConfig
from doodledashboard.displays.display import Display
from tests.doodledashboard.it.support import CliTestCase


class DummyDisplay(Display):

    def __init__(self, interval):
        self._interval = interval

    def get_interval(self):
        return self._interval

    def draw(self, notification):
        pass

    @staticmethod
    def get_supported_notifications():
        return []

    def __str__(self):
        return "Display (interval=%s)" % self._interval


class DummyDisplayConfig(ComponentConfig, DisplayConfig):
    _DEFAULT_INTERVAL = 5

    @staticmethod
    def get_id():
        return "test-display-with-interval"

    def create(self, options):
        interval = options.get("seconds-per-notifications", self._DEFAULT_INTERVAL)
        return DummyDisplay(interval)


@pytest.mark.usefixtures
class StartCommand(CliTestCase):
    dashboard_one = """
    dashboard:
      display:
        type: console
        options:
          seconds-per-notifications: 0
      data-feeds:
        - type: text
          options:
            text: Test value 1

      notifications:
        - name: Notification 1
          type: text-from-message
          filters:
            - type: message-contains-text
              options:
                text: 2
    """

    dashboard_two = """
    dashboard:
      data-feeds:
        - type: text
          options:
            text: Test value 2
      notifications:
        - name: Notification 2
          type: text-from-message
          filters:
            - type: message-contains-text
              options:
                text: 1
    """

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_notification_in_each_config_display_message_from_other_config(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.dashboard_two)
            self.http_server.serve_content(self.dashboard_one)

            result = self.call_cli(runner, start, "config.yml %s --once" % self.http_server.url)

        self.assertIn("Test value 2", result.output)
        self.assertIn("Test value 1", result.output)
        self.assertEqual(0, result.exit_code)

    def test_last_config_takes_precedence(self):
        first_config = """
        dashboard:
          display:
            type: test-display-with-interval
            options:
              seconds-per-notifications: 999
        """

        second_config = """
        dashboard:
          display:
            type: test-display-with-interval
            options:
              seconds-per-notifications: 123
        """

        StaticComponentSource.add(DummyDisplayConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", first_config)
            self.http_server.serve_content(second_config)

            result = self.call_cli(runner, start, "config.yml %s --once" % self.http_server.url)

        self.assertIn("Display (interval=123)", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
