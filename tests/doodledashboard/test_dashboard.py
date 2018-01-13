import unittest

from mock import Mock, mock

from doodledashboard.dashboard import Dashboard


class TestAbstractDashboard(unittest.TestCase):
    class TestDashboard(Dashboard):
        def __init__(self, display, filtered_handlers, repositories):
            Dashboard.__init__(self, display)
            self._filtered_handlers = filtered_handlers
            self._repositories = repositories

        def get_update_interval(self):
            return 0

        def get_filtered_handlers(self):
            return self._filtered_handlers

        def get_repositories(self):
            return self._repositories

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_messages_from_repositories_are_passed_to_handlers_filter(self, itertools_cycle_function):
        message_1 = Mock()
        message_2 = Mock()
        message_3 = Mock()

        repositories = [Mock(), Mock()]
        repositories[0].get_latest_messages.return_value = [message_1, message_2]
        repositories[1].get_latest_messages.return_value = [message_3]

        handlers = [{'handler': Mock(), 'filter_chain': None}]

        TestAbstractDashboard.TestDashboard(Mock(), handlers, repositories).start()

        handlers[0]['handler'].update.assert_called_with([message_1, message_2, message_3])

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_get_latest_messages_called_for_all_repositories_when_start_called(self, itertools_cycle_function):
        display = Mock()
        handlers = [{'handler': Mock(), 'filter_chain': None}]

        repositories = [self._create_emtpy_repository(),
                        self._create_emtpy_repository()]

        TestAbstractDashboard.TestDashboard(display, handlers, repositories).start()

        repositories[0].get_latest_messages.assert_called()
        repositories[1].get_latest_messages.assert_called()

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_display_passed_to_handler(self, itertools_cycle_function):
        display = Mock()
        handlers = [{'handler': Mock(), 'filter_chain': None}]

        TestAbstractDashboard.TestDashboard(display, handlers, [self._create_emtpy_repository()]).start()

        handlers[0]['handler'].draw.assert_called_with(display)

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_messages_from_repositories_passed_to_filter(self, itertools_cycle_function):
        message_1 = Mock()
        message_2 = Mock()
        message_3 = Mock()

        repositories = [Mock(), Mock()]
        repositories[0].get_latest_messages.return_value = [message_1, message_2]
        repositories[1].get_latest_messages.return_value = [message_3]

        handlers = [{'handler': Mock(), 'filter_chain': Mock()}]

        TestAbstractDashboard.TestDashboard(Mock(), handlers, repositories).start()

        handlers[0]['filter_chain'].filter.assert_called_with([message_1, message_2, message_3])

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_messages_from_filters_passed_to_handler_update(self, itertools_cycle_function):
        handlers = [{'handler': Mock(), 'filter_chain': Mock()},
                    {'handler': Mock(), 'filter_chain': Mock()}]

        messages_1 = [Mock()]
        messages_2 = [Mock(), Mock()]
        handlers[0]['filter_chain'].filter.return_value = messages_1
        handlers[1]['filter_chain'].filter.return_value = messages_2

        TestAbstractDashboard.TestDashboard(Mock(), handlers, [self._create_emtpy_repository()]).start()

        handlers[0]['handler'].update.assert_called_with(messages_1)
        handlers[1]['handler'].update.assert_called_with(messages_2)

    @staticmethod
    def _create_emtpy_repository():
        repository = Mock()
        repository.get_latest_messages.return_value = []
        return repository

if __name__ == '__main__':
    unittest.main()
