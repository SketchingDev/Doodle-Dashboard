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
        handlers = [Mock(), Mock()]
        handlers[0].get_tag.return_value = '1'
        handlers[1].get_tag.return_value = '2'

        message_1 = TestAbstractDashboard.create_mock_message_with_text('1')
        message_2 = TestAbstractDashboard.create_mock_message_with_text('2')
        message_3 = TestAbstractDashboard.create_mock_message_with_text('2')

        repositories = [Mock(), Mock()]
        repositories[0].get_latest_messages.return_value = [message_1, message_2]
        repositories[1].get_latest_messages.return_value = [message_3]

        TestAbstractDashboard.TestDashboard(display, handlers, repositories).start()

        handlers[0].draw.assert_called_with(display, [message_1])
        handlers[1].draw.assert_called_with(display, [message_2, message_3])

    @staticmethod
    def create_mock_message_with_text(text):
        message = Mock()
        message.get_text.return_value = text
        return message

    # @staticmethod
    # def return_argument(values):
    #     return values

if __name__ == '__main__':
    unittest.main()
