import yaml
from yaml import YAMLError


class InvalidSecretsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SecretsYamlParsingError(InvalidSecretsException):
    def __init__(self, parsing_exception, secrets_path):
        self.parsing_exception = parsing_exception
        self.secrets_path = secrets_path


def read_secrets(file_path):
    with open(file_path, "r") as f:
        secrets_yaml = f.read()

    try:
        return yaml.safe_load(secrets_yaml)
    except YAMLError as err:
        raise SecretsYamlParsingError(err, file_path)
