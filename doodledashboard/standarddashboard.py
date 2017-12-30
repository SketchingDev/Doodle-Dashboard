from slackclient import SlackClient

from doodledashboard.lucas.datasources.slack import SlackRepository
from doodledashboard.lucas.handlers.filters import MessageContainsTextFilter
from lucas.dashboard import Dashboard
from lucas.handlers.weather.weather import WeatherHandler


class StandardDashboard(Dashboard):
    def __init__(self, slack_config, display, shelve):
        Dashboard.__init__(self, display)
        self._slack_config = slack_config
        self._shelve = shelve

    def get_update_interval(self):
        return 8

    def get_filtered_handlers(self):
        return [{'handler': WeatherHandler(self._shelve), 'filter_chain': MessageContainsTextFilter('#weather')}]

    def get_repositories(self):
        slack_client = SlackClient(self._slack_config.get_token())
        channel = self._slack_config.get_channel_name()

        return [SlackRepository(slack_client, channel)]
