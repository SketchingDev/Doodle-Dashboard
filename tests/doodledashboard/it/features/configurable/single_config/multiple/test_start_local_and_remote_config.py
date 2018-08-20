import pytest
import unittest

from click.testing import CliRunner
from pytest_localserver import http

from doodledashboard.cli import start
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from tests.doodledashboard.it.support.cli_test_case import CliTestCase
from tests.doodledashboard.it.support.displays import DisplayWithNotificationSupport


@pytest.mark.usefixtures
class TestCliStartLocalAndRemoteConfig(CliTestCase):
    dashboard_one = """
    interval: 0
    display: test-display-all-functionality
    data-feeds:
      - source: text
        text: Test value 1

    notifications:
        - title: Notification 1
          type: text
          update-with:
            name: text-from-message
            filter-messages:
                - type: message-contains-text
                  text: 2
    """

    dashboard_two = """
        data-feeds:
          - source: text
            text: Test value 2

        notifications:
            - title: Notification 2
              type: text
              update-with:
                name: text-from-message
                filter-messages:
                - type: message-contains-text
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
        StaticComponentLoader.displays.append(DisplayWithNotificationSupport)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.dashboard_two)
            self.http_server.serve_content(self.dashboard_one)

            result = self.call_cli(runner, start, "config.yml %s --once" % self.http_server.url)

        self.assertIn("(title=Notification 1, text=Test value 2)", result.output)
        self.assertIn("(title=Notification 2, text=Test value 1)", result.output)
        self.assertEqual(0, result.exit_code)

    def test_last_config_takes_precedence(self):
        first_config = """
        interval: 999
        display: test-display-all-functionality
        """

        second_config = """
        interval: 123
        """

        StaticComponentLoader.displays.append(DisplayWithNotificationSupport)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", first_config)
            self.http_server.serve_content(second_config)

            result = self.call_cli(runner, start, "config.yml %s --once" % self.http_server.url)

        self.assertIn("Interval: 123", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
