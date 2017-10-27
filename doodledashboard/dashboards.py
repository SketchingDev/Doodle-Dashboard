from doodledashboard.lucas.handlers.quote.quote import QuoteHandler
from lucas.dashboard import Dashboard
from lucas.factories import ClientFactory
from lucas.handlers.steps.steps import StepsHandler


class StandardDashboard(Dashboard):
    def __init__(self, slack_config, display, shelve):
        Dashboard.__init__(self, slack_config, display)
        self._shelve = shelve

    def get_update_interval(self):
        return 5

    def get_handlers(self):
        return [QuoteHandler(self._shelve), StepsHandler(self._shelve)]

    def get_client(self, slack_config):
        return ClientFactory().create(slack_config)
