import json
import pytest
import unittest
from click.testing import CliRunner
from pytest_localserver import http

from doodledashboard.cli import view
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


@pytest.mark.usefixtures
class TestCliViewRemoteConfig(CliTestCase):

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_invalid_display_shows_error(self):
        config_with_invalid_display = """
        display: none
        """
        self.http_server.serve_content(config_with_invalid_display)

        result = self.call_cli(CliRunner(), view, "datafeeds %s" % self.http_server.url)

        self.assertIn(
            "Cannot find the display 'none'. Have you run `pip install` for the display you're trying to use?",
            result.output)
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
        data-feeds:
          - source: text
            text: Test value 1
        notifications:
          - title: Print any message containing 1
            type: text
            update-with:
              name: text-from-message
              filter-messages:
                - type: message-contains-text
                  text: 1
        """
        self.http_server.serve_content(config)

        result = self.call_cli(CliRunner(), view, "notifications %s" % self.http_server.url)

        data = json.loads(result.output)
        self.assertEqual(1, len(data["notifications"]), "There should be one notification")
        notification = data["notifications"][0]

        self.assertEqual("Text notification (title=Print any message containing 1, text=)",
                         notification["notification-before"],
                         "Notification before being passed filtered message")
        self.assertEqual("Text notification (title=Print any message containing 1, text=Test value 1)",
                         notification["notification-after"],
                         "Notification after being passed filtered message")


if __name__ == '__main__':
    unittest.main()
