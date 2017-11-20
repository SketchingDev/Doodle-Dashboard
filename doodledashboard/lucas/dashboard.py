import time

import itertools


class Dashboard:
    def __init__(self, slack_config, display):
        self._slack_config = slack_config
        self._display = display

    def start(self):
        repository = self.get_repository(self._slack_config)

        update_interval = self.get_update_interval()
        for handler in itertools.cycle(self.get_handlers()):
            messages = repository.get_latest_messages()
            messages = Dashboard._filter_messages_containing_text(messages, handler.get_tag())

            handler.draw(self._display, messages)

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
