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

        filtered_handlers = self.get_filtered_handlers()
        self._logger.info('%s filtered handlers loaded' % len(filtered_handlers))

        messages = []
        update_interval = self.get_update_interval()
        for filtered_handler in itertools.cycle(filtered_handlers):

            if filtered_handler is filtered_handlers[0]:  # Is at beginning
                messages = self._collect_all_messages(repositories)

            handler = filtered_handler['handler']
            filter_chain = filtered_handler['filter_chain']

            handlers_messages = filter_chain.filter(messages) if filter_chain else messages

            handler.update(handlers_messages)
            handler.draw(self._display)

            time.sleep(update_interval)

    def _collect_all_messages(self, repositories):
        messages = []
        for repository in repositories:
            messages += repository.get_latest_messages()

        return messages

    def get_update_interval(self):
        raise NotImplementedError('Implement this method')

    def get_filtered_handlers(self):
        raise NotImplementedError('Implement this method')

    def get_repositories(self):
        raise NotImplementedError('Implement this method')
