import logging
import yaml


class SecretNotFound(Exception):
    def __init__(self, data_feed, missing_token):
        self.data_feed = data_feed
        self.missing_token = missing_token

    # def __str__(self):
    #     return "Secret Not Found (missing_token=%s, data_feed=%s)" % (self.missing_token, self.data_feed)


class InvalidSecretsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SecretsYamlParsingError(InvalidSecretsException):
    def __init__(self, parsing_exception, secrets_path):
        super().__init__("Error parsing YAML file %s due to %s" % (secrets_path, parsing_exception))
        self.parsing_exception = parsing_exception
        self.secrets_path = secrets_path


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
