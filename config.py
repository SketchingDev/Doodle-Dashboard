class AppConfig:
    def __init__(self, config):
        self._config = config

    def read(self, configs):
        self._config.read(configs)

    def get_slack_token(self):
        return self._config.get('Slack', 'Token')

    def get_dashboard_channel_name(self):
        return self._config.get('Slack', 'Channel')

    def get_update_interval(self):
        return self._config.getint('Dashboard', 'UpdateInterval')