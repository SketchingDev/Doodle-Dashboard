from doodledashboard.configuration.config import ConfigSection
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class SecretLeaker(DataFeed):

    def __init__(self, secret_id):
        super().__init__()
        self._secret_id = secret_id

    def get_latest_messages(self):
        secrets = self.get_secret_store()

        if self._secret_id in secrets:
            return [Message(secrets[self._secret_id])]
        else:
            return []

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
