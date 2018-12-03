import unittest

import json
from click.testing import CliRunner

from doodledashboard.cli import start, view
from doodledashboard.component import StaticComponentSource, ComponentConfig, DataFeedConfig
from doodledashboard.datafeeds.datafeed import DataFeed, Message
from doodledashboard.secrets_store import SecretNotFound
from tests.doodledashboard.it.support import CliTestCase


class SecretLeaker(DataFeed):

    def __init__(self, secret_key):
        super().__init__()
        self._secret_key = secret_key

    def get_latest_messages(self):
        secret_value = self.secret_store.get(self._secret_key)

        if secret_value:
            return [Message(secret_value)]
        else:
            raise SecretNotFound(self, self._secret_key)

    def required_secrets(self):
        return [self._secret_key]

    def __str__(self):
        return "SecretLeaker"


class SecretLeakerConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "leak-secrets"

    def create(self, options):
        return SecretLeaker(options["secret-id"])


class StartCommand(CliTestCase):
    dashboard_that_outputs_messages_containing_test = """
        dashboard:
          display:
            type: console
            options:
              seconds-per-notifications: 0
          data-feeds:
            - type: leak-secrets
              options:
                secret-id: twitter-api
          notifications:
            - title: Leaked secret
              type: text-from-message
        """

    def test_secrets_available_to_data_feed(self):
        secrets = "twitter-api: This secret has been printed to the console"

        StaticComponentSource.add(SecretLeakerConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", self.dashboard_that_outputs_messages_containing_test)
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, start, "--once config.yml --secrets secrets.yml")

        self.assertIn("This secret has been printed to the console", result.output)
        self.assertEqual(0, result.exit_code)

    def test_friendly_error_message_output_if_data_feed_throws_secret_not_found(self):
        secrets = ""
        config_for_notification_that_prints_password = """
        dashboard:
          data-feeds:
            - type: leak-secrets
              options:
                secret-id: twitter-api
        """

        StaticComponentSource.add(SecretLeakerConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_for_notification_that_prints_password)
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, start, "--once config.yml --secrets secrets.yml")

        err_msg = "The secret 'twitter-api' is missing from your secrets file according to the data feed SecretLeaker"
        self.assertIn(err_msg, result.output)
        self.assertEqual(1, result.exit_code)

    def test_secrets_not_found_info_shown_for_default_secrets_not_existing_when_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, "--once --verbose")

        self.assertIn("Secrets file not found: /.doodledashboard/secrets", result.output)
        self.assertEqual(0, result.exit_code)

    def test_secrets_not_found_info_not_shown_for_default_secrets_not_existing_when_not_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, "--once")

        self.assertNotIn("Secrets file not found: /.doodledashboard/secrets", result.output)
        self.assertEqual(0, result.exit_code)

    def test_useful_error_if_secret_file_provided_does_not_exist(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, start, "--once --secrets i-dont-exist.yml")

        self.assertIn("Path \"i-dont-exist.yml\" does not exist.", result.output)
        self.assertEqual(2, result.exit_code)

    def test_useful_error_if_secret_file_contains_invalid_yaml(self):
        secrets = ":"

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, start, "--once --secrets secrets.yml")

        self.assertIn("Error while parsing", result.output)
        self.assertEqual(1, result.exit_code)


class ViewCommand(CliTestCase):

    def test_secrets_available_to_data_feeds(self):
        secrets = "twitter-api: This is a secret"
        config_for_notification_that_prints_password = """
        dashboard:
          data-feeds:
            - type: leak-secrets
              options:
                secret-id: twitter-api
        """

        StaticComponentSource.add(SecretLeakerConfig)

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
        dashboard:
           data-feeds:
             - type: leak-secrets
               options:
                 secret-id: twitter-api
        """

        StaticComponentSource.add(SecretLeakerConfig)

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("config.yml", config_for_notification_that_prints_password)
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, view, "datafeeds config.yml --secrets secrets.yml")

        err_msg = "The secret 'twitter-api' is missing from your secrets file according to the data feed SecretLeaker"
        self.assertIn(err_msg, result.output)
        self.assertEqual(1, result.exit_code)

    def test_secrets_not_found_info_shown_for_default_secrets_not_existing_when_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "datafeeds --verbose")

        self.assertIn("Secrets file not found: /.doodledashboard/secrets", result.output)
        self.assertEqual(0, result.exit_code)

    def test_secrets_not_found_info_not_shown_for_default_secrets_not_existing_when_not_verbose(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view)

        self.assertNotIn("Secrets file not found: /.doodledashboard/secrets", result.output)
        self.assertEqual(2, result.exit_code)

    def test_useful_error_if_secret_file_provided_does_not_exist(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, view, "datafeeds --secrets i-dont-exist.yml")

        self.assertIn("Path \"i-dont-exist.yml\" does not exist.", result.output)
        self.assertEqual(2, result.exit_code)

    def test_useful_error_if_secret_file_contains_invalid_yaml(self):
        secrets = ":"

        runner = CliRunner()
        with runner.isolated_filesystem():
            self.save_file("secrets.yml", secrets)
            result = self.call_cli(runner, view, "datafeeds --secrets secrets.yml")

        self.assertIn("Error while parsing", result.output)
        self.assertEqual(1, result.exit_code)


if __name__ == '__main__':
    unittest.main()
