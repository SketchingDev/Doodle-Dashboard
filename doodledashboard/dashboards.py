from lucas.handlers.weather.weather import WeatherHandler
from lucas.dashboard import Dashboard
from lucas.factories import ClientFactory
from lucas.handlers.steps.steps import StepsHandler


class StandardDashboard(Dashboard):
    def __init__(self, slack_config, display, shelve):
        Dashboard.__init__(self, slack_config, display)
        self._shelve = shelve

    def get_update_interval(self):
        return 8

    def get_handlers(self):
        return [StepsHandler(self._shelve), WeatherHandler(self._shelve)]

    def get_client(self, slack_config):
        return ClientFactory().create(slack_config)
