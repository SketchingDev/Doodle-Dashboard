import time

import itertools
import logging


class Dashboard:
    def __init__(self, slack_config, display):
        self._slack_config = slack_config
        self._display = display
        self._logger = logging.getLogger('raspberry_pi_dashboard.Dashboard')

    def start(self):
        repository = self.get_repository(self._slack_config)

        handlers = self.get_handlers()
        self._logger.info('%s handlers loaded' % len(handlers))

        messages = []
        update_interval = self.get_update_interval()
        for handler in itertools.cycle(handlers):
            if handlers[0] is handler:
                messages = repository.get_latest_messages()

            handler_messages = Dashboard._filter_messages_containing_text(messages, handler.get_tag())
            handler.draw(self._display, handler_messages)

            time.sleep(update_interval)

    def get_update_interval(self):
        raise NotImplementedError('Implement this method')

    def get_handlers(self):
        raise NotImplementedError('Implement this method')

    def get_repository(self, config):
        raise NotImplementedError('Implement this method')

    @staticmethod
    def _filter_messages_containing_text(messages, text):
        return [m for m in messages if text in m.get_text()]
