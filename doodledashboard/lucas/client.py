import ConfigParser


class SlackConfig:
    def __init__(self, config):
        self._config = config

    def get_token(self):
        return self._config.get('Slack', 'Token')

    def get_channel_name(self):
        return self._config.get('Slack', 'Channel')

    @staticmethod
    def create_from_file(file_path):
        config = ConfigParser.ConfigParser()
        config.read(file_path)

        return SlackConfig(config)
