import unittest

from mock import Mock, mock

from doodledashboard.lucas.dashboard import Dashboard


class TestAbstractDashboard(unittest.TestCase):
    class TestDashboard(Dashboard):
        def __init__(self, display, handlers, repositories):
            Dashboard.__init__(self, display)
            self._handlers = handlers
            self._repositories = repositories

        def get_update_interval(self):
            return 0

        def get_handlers(self):
            return self._handlers

        def get_repositories(self):
            return self._repositories

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_messages_from_repositories_are_passed_to_handlers_filter(self, itertools_cycle_function):
        display = Mock()
        handler_1 = Mock()

        message_1 = Mock()
        message_2 = Mock()
        message_3 = Mock()

        repository_1 = Mock()
        repository_2 = Mock()
        repository_1.get_latest_messages.return_value = [message_1, message_2]
        repository_2.get_latest_messages.return_value = [message_3]

        TestAbstractDashboard.TestDashboard(display, [handler_1], [repository_1, repository_2]).start()

        handler_1.filter.assert_called_with([message_1, message_2, message_3])

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_get_latest_messages_called_for_all_repositories_when_start_called(self, itertools_cycle_function):
        display = Mock()
        handlers = [Mock()]
        repositories = [Mock(), Mock()]

        repositories[0].get_latest_messages.return_value = []
        repositories[1].get_latest_messages.return_value = []

        TestAbstractDashboard.TestDashboard(display, handlers, repositories).start()

        repositories[0].get_latest_messages.assert_called()
        repositories[1].get_latest_messages.assert_called()

    @mock.patch('itertools.cycle', side_effect=(lambda values: values))
    def test_messages_from_repositories_with_tags_passed_to_handlers(self, itertools_cycle_function):
        display = Mock()

        message_1 = Mock()
        message_2 = Mock()
        message_3 = Mock()

        handlers = [Mock(), Mock()]
        handlers[0].filter.return_value = [message_1]
        handlers[1].filter.return_value = [message_2, message_3]

        repository_1 = Mock()
        repository_1.get_latest_messages.return_value = []

        TestAbstractDashboard.TestDashboard(display, handlers, [repository_1]).start()

        handlers[0].draw.assert_called_with(display, [message_1])
        handlers[1].draw.assert_called_with(display, [message_2, message_3])


if __name__ == '__main__':
    unittest.main()
