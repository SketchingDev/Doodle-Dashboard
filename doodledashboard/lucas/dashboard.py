import time

import itertools


class Dashboard:
    def __init__(self, slack_config, display):
        self._slack_config = slack_config
        self._display = display

    def start(self):
        client = self.get_client(self._slack_config)

        if not client.connect():
            raise ValueError("Failed to connect to Slack. Connected to the internet and using the correct Slack token?")
        else:
            update_interval = self.get_update_interval()
            for handler in itertools.cycle(self.get_handlers()):
                messages = client.find_messages_by_text_content(handler.get_tag())

                handler.draw(self._display, messages)

                time.sleep(update_interval)

    def get_update_interval(self):
        raise NotImplementedError('Implement this method')

    def get_handlers(self):
        raise NotImplementedError('Implement this method')

    def get_client(self, config):
        raise NotImplementedError('Implement this method')
