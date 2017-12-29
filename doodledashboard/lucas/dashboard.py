import itertools
import logging
import time


class Dashboard:
    def __init__(self, display):
        self._display = display
        self._logger = logging.getLogger('doodle_dashboard.Dashboard')

    def start(self):
        repositories = self.get_repositories()
        self._logger.info('%s repositories loaded' % len(repositories))

        handlers = self.get_handlers()
        self._logger.info('%s handlers loaded' % len(handlers))

        messages = []
        update_interval = self.get_update_interval()
        for handler in itertools.cycle(handlers):
            is_at_beginning = handlers[0] is handler
            if is_at_beginning:
                messages = self._collect_all_messages(repositories)

            handler.draw(self._display, handler.filter(messages))

            time.sleep(update_interval)

    def _collect_all_messages(self, repositories):
        messages = []
        for repository in repositories:
            messages += repository.get_latest_messages()

        return messages

    def get_update_interval(self):
        raise NotImplementedError('Implement this method')

    def get_handlers(self):
        raise NotImplementedError('Implement this method')

    def get_repositories(self):
        raise NotImplementedError('Implement this method')
