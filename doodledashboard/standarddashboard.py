from slackclient import SlackClient

from doodledashboard.lucas.datasources.rss import RssFeed
from doodledashboard.lucas.datasources.slack import SlackRepository
from doodledashboard.lucas.handlers.filters import MessageMatchesRegexFilter
from lucas.dashboard import Dashboard
from lucas.handlers.weather.weather import WeatherHandler


class StandardDashboard(Dashboard):
    _WEATHER_URL = 'http://open.live.bbc.co.uk/weather/feeds/en/2643743/observations.rss'
    _EIGHT_SECONDS = 8

    def __init__(self, slack_config, display, shelve):
        Dashboard.__init__(self, display)
        self._slack_config = slack_config
        self._shelve = shelve

    def get_update_interval(self):
        return StandardDashboard._EIGHT_SECONDS

    def get_filtered_handlers(self):
        return [{
            'handler': WeatherHandler(self._shelve), 'filter_chain': MessageMatchesRegexFilter('weather')
        }]

    def get_repositories(self):
        return [
            self._create_slack_repository(),
            RssFeed(StandardDashboard._WEATHER_URL)
        ]

    def _create_slack_repository(self):
        slack_client = SlackClient(self._slack_config.get_token())
        channel = self._slack_config.get_channel_name()

        return SlackRepository(slack_client, channel)

