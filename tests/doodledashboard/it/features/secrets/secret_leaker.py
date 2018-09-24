from doodledashboard.configuration.config import ConfigSection
from doodledashboard.datafeeds.datafeed import DataFeed, Message
from doodledashboard.secrets_store import SecretNotFound


class SecretLeaker(DataFeed):

    def __init__(self, secret_key):
        super().__init__()
        self._secret_key = secret_key

    def get_latest_messages(self):
        secrets = self.get_secret_store()

        if self._secret_key in secrets:
            return [Message(secrets[self._secret_key])]
        else:
            raise SecretNotFound(self, self._secret_key)

    def required_secrets(self):
        return [self._secret_key]

    def __str__(self):
        return "SecretLeaker"

    @staticmethod
    def get_config_factory():
        return SecretLeakerConfig()


class SecretLeakerConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "source", "leak-secrets"

    def create(self, config_section):
        return SecretLeaker(config_section["secret-id"])
