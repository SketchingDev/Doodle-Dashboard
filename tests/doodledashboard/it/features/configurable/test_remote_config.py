import json
import pytest
import unittest

from click.testing import CliRunner
from pytest_localserver import http

from doodledashboard.cli import start, view
from tests.doodledashboard.it.support import CliTestCase


@pytest.mark.usefixtures
class StartCommand(CliTestCase):

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_single_config_with_invalid_display_shows_error(self):
        config_with_invalid_display = """
        dashboard:
          display:
            type: non-existent
        """
        self.http_server.serve_content(config_with_invalid_display)

        result = self.call_cli(CliRunner(), start, self.http_server.url)

        self.assertIn(
            "Cannot find the display 'non-existent'. Have you run `pip install` for the display you're trying to use?",
            result.output)
        self.assertEqual(1, result.exit_code)

    def test_malformed_config_displays_error(self):
        malformed_display = """
        :
        """
        self.http_server.serve_content(malformed_display)

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, self.http_server.url)

        self.assertIn("Error while parsing a block mapping", result.output)
        self.assertEqual(1, result.exit_code)

    def test_notification_with_datafeed_loaded_from_config(self):
        config_with_single_notification = """
        dashboard:
          display:
            type: console
            options:
              seconds-per-notifications: 0
          data-feeds:
            - type: text
              options:
                text:
                  - Test Message 1
          notifications:
            - title: Print message
              type: text-from-message
        """
        self.http_server.serve_content(config_with_single_notification)

        result = self.call_cli(CliRunner(), start, "%s --once" % self.http_server.url)

        self.assertIn("1 notifications loaded", result.output)
        self.assertIn("Test Message 1", result.output)
        self.assertEqual(0, result.exit_code)


@pytest.mark.usefixtures
class ViewCommand(CliTestCase):

    @staticmethod
    def _disable_werkzeug_logging_to_console():
        import logging
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

        cls._disable_werkzeug_logging_to_console()

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_invalid_display_shows_error(self):
        config_with_invalid_display = """
        dashboard:
          display:
            type: non-existent
        """
        self.http_server.serve_content(config_with_invalid_display)

        result = self.call_cli(CliRunner(), view, "datafeeds %s" % self.http_server.url)

        msg = "Cannot find the display 'non-existent'. Have you run `pip install` for the display you're trying to use?"
        self.assertIn(msg, result.output)
        self.assertEqual(1, result.exit_code)

    def test_malformed_config_displays_error(self):
        malformed_config = """
        :
        """
        self.http_server.serve_content(malformed_config)

        result = self.call_cli(CliRunner(), view, "datafeeds %s" % self.http_server.url)

        self.assertIn("Error while parsing a block mapping", result.output)
        self.assertEqual(1, result.exit_code)

    def test_notification_with_datafeed_and_filter_loaded_from_config(self):
        config = """
        dashboard:
          data-feeds:
            - type: text
              options:
                text:
                  - Test Message 1
          notifications:
            - name: Print message
              type: text-from-message
        """
        self.http_server.serve_content(config)

        result = self.call_cli(CliRunner(), view, "notifications %s" % self.http_server.url)

        data = json.loads(result.output)
        self.assertEqual(1, len(data["notifications"]), "There should be one notification")
        notification = data["notifications"][0]

        self.assertEqual("Text (name=Print message, text=Test Message 1)",
                         notification["notification"],
                         "Notification after being passed filtered message")


if __name__ == '__main__':
    unittest.main()
