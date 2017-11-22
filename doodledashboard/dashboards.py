from slackclient import SlackClient

from doodledashboard.lucas.handlers.bank.bank import BankHandler
from doodledashboard.lucas.repositories import SlackRepository
from lucas.handlers.weather.weather import WeatherHandler
from lucas.dashboard import Dashboard
from lucas.handlers.steps.steps import StepsHandler


class StandardDashboard(Dashboard):
    def __init__(self, slack_config, display, shelve):
        Dashboard.__init__(self, slack_config, display)
        self._shelve = shelve

    def get_update_interval(self):
        return 8

    def get_handlers(self):
        return [StepsHandler(self._shelve), WeatherHandler(self._shelve), BankHandler(self._shelve)]

    def get_repository(self, slack_config):
        slack_client = SlackClient(slack_config.get_token())
        channel = slack_config.get_channel_name()

        return SlackRepository(slack_client, channel)
