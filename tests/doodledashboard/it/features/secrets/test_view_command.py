import json
import unittest

from click.testing import CliRunner

from doodledashboard.cli import view
from doodledashboard.configuration.component_loaders import StaticComponentLoader
from tests.doodledashboard.it.features.secrets.secret_leaker import SecretLeaker
from tests.doodledashboard.it.support.cli_test_case import CliTestCase


class TestSecretsForViewCommand(CliTestCase):
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

    def test_secrets_available_to_data_feeds(self):
        secrets = "twitter-api: This is a secret"
        config_for_notification_that_prints_password = """
        data-feeds:
          - source: leak-secrets
            secret-id: twitter-api
        """

        StaticComponentLoader.datafeeds.append(SecretLeaker)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_for_notification_that_prints_password)
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, view, "datafeeds config.yml --secrets secrets.yml")

        data = json.loads(result.output)
        self.assertEqual(1, len(data["source-data"]), "Source data should contain 1 message")
        self.assertEqual("This is a secret", data["source-data"][0]["text"], "Secret is in message")
        self.assertEqual(0, result.exit_code)

    def test_friendly_error_message_output_if_data_feed_throws_secret_not_found(self):
        secrets = ""
        config_for_notification_that_prints_password = """
                data-feeds:
                  - source: leak-secrets
                    secret-id: twitter-api
                """

        StaticComponentLoader.datafeeds.append(SecretLeaker)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_for_notification_that_prints_password)
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, view, "datafeeds config.yml --secrets secrets.yml")

        self.assertIn(
            "The secret 'twitter-api' is missing from your secrets file according to the data feed SecretLeaker",
            result.output
        )
        self.assertEqual(1, result.exit_code)

    def test_secrets_not_found_info_shown_for_default_secrets_not_existing_when_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "datafeeds --verbose")

        self.assertIn(
            "Secrets file not found: /.doodledashboard/secrets",
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_secrets_not_found_info_not_shown_for_default_secrets_not_existing_when_not_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view)

        self.assertNotIn(
            "Secrets file not found: /.doodledashboard/secrets",
            result.output
        )
        self.assertEqual(2, result.exit_code)

    def test_useful_error_if_secret_file_provided_does_not_exist(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "datafeeds --secrets i-dont-exist.yml")

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
            result = self.call_cli(runner, view, "datafeeds --secrets secrets.yml")

        self.assertIn(
            "Error while parsing",
            result.output
        )
        self.assertEqual(1, result.exit_code)


if __name__ == '__main__':
    unittest.main()
