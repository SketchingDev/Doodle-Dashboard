import pytest
import unittest

from click.testing import CliRunner
from pytest_localserver import http

from doodledashboard.cli import start
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

    def test_single_config_with_invalid_display_shows_error(self):
        config_with_invalid_display = """
        display: none
        """
        self.http_server.serve_content(config_with_invalid_display)

        result = self.call_cli(CliRunner(), start, self.http_server.url)

        self.assertIn(
            "Cannot find the display 'none'. Have you run `pip install` for the display you're trying to use?",
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

    def test_default_interval_used_if_none_provided(self):
        config_without_interval = ""
        self.http_server.serve_content(config_without_interval)

        result = self.call_cli(CliRunner(), start, "%s --once" % self.http_server.url)

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
        self.http_server.serve_content(config_with_single_notification)

        result = self.call_cli(CliRunner(), start, "%s --once" % self.http_server.url)

        self.assertIn("1 notifications loaded", result.output)
        self.assertIn("Test Message 1", result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
