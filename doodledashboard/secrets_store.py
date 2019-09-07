import logging
import yaml


class SecretNotFound(Exception):
    def __init__(self, data_feed, missing_token):
        self._data_feed = data_feed
        self._missing_token = missing_token

    @property
    def data_feed(self):
        return self._data_feed

    @property
    def missing_token(self):
        return self._missing_token


class InvalidSecretsException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)


class SecretsYamlParsingError(InvalidSecretsException):
    def __init__(self, parsing_exception, secrets_path):
        super().__init__("Error parsing YAML file %s due to %s" % (secrets_path, parsing_exception))
        self._parsing_exception = parsing_exception
        self._secrets_path = secrets_path

    @property
    def parsing_exception(self):
        return self._parsing_exception

    @property
    def secrets_path(self):
        return self._secrets_path


def read_secrets(file_path):
    with open(file_path, "r") as f:
        secrets_yaml = f.read()

    try:
        return yaml.safe_load(secrets_yaml)
    except yaml.YAMLError as err:
        raise SecretsYamlParsingError(err, file_path)


def try_read_secrets_file(secrets_file):
    secrets = {}

    try:
        secrets = read_secrets(secrets_file)
    except FileNotFoundError:
        logger = logging.getLogger(__name__)
        logger.info("Secrets file not found: %s", secrets_file)

    return secrets if secrets is not None else {}
