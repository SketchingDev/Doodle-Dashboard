import unittest
from click.testing import CliRunner

from doodledashboard.cli import start
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from tests.doodledashboard.it.features.secrets.dummy_data_feeds import SecretLeaker
from tests.doodledashboard.it.support.cli_test_case import CliTestCase
from tests.doodledashboard.it.support.displays import DisplayWithNotificationSupport


class TestSecretsForStartCommand(CliTestCase):
    dashboard_that_outputs_messages_containing_test = """
    interval: 0
    display: test-display-all-functionality
    data-feeds:
      - source: leak-secrets
        secret-id: twitter-api

    notifications:
      - title: Leaked secret
        type: text
        update-with:
          name: text-from-message
    """

    def test_secrets_available_to_data_feed(self):
        secrets = "twitter-api: This is a secret"

        StaticComponentLoader.displays.append(DisplayWithNotificationSupport)
        StaticComponentLoader.datafeeds.append(SecretLeaker)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.dashboard_that_outputs_messages_containing_test)
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, start, "--once config.yml --secrets secrets.yml")

        self.assertIn(
            "Displaying Text notification (title=Leaked secret, text=This is a secret)",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_secrets_not_found_info_shown_for_default_secrets_not_existing_when_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, "--once --verbose")

        self.assertIn(
            "Secrets file not found: /.doodledashboard/secrets",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_secrets_not_found_info_not_shown_for_default_secrets_not_existing_when_not_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, "--once")

        self.assertNotIn(
            "Secrets file not found: /.doodledashboard/secrets",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_useful_error_if_secret_file_provided_does_not_exist(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, "--once --secrets i-dont-exist.yml")

        self.assertIn(
            "Path \"i-dont-exist.yml\" does not exist.",
            result.output
        )
        self.assertEqual(2, result.exit_code)

    def test_useful_error_if_secret_file_contains_invalid_yaml(self):
        secrets = ":"

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, start, "--once --secrets secrets.yml")

        self.assertIn(
            "Error while parsing",
            result.output
        )
        self.assertEqual(1, result.exit_code)


if __name__ == '__main__':
    unittest.main()
