import unittest

from mock import Mock

from doodledashboard.dashboard_runner import Notification


class TestNotification(unittest.TestCase):

    def test_filter_chain_passed_messages(self):
        messages = [Mock(), Mock()]

        filter_chain = Mock()

        notification = Notification(Mock())
        notification.set_filter_chain(filter_chain)

        notification.handle_messages(Mock(), messages)

        filter_chain.filter.assert_called_with(messages)

    def test_messages_from_filter_passed_handlers_update_method(self):
        messages = [Mock(), Mock()]

        filter_chain = Mock()
        filter_chain.filter.return_value = messages

        handler = Mock()

        notification = Notification(handler)
        notification.set_filter_chain(filter_chain)
        notification.handle_messages(Mock(), messages)

        handler.update.assert_called_with(messages)

    def test_messages_passed_to_handlers_update_method_if_filter_chain_is_not_set(self):
        messages = [Mock(), Mock()]

        handler = Mock()

        notification = Notification(handler)
        notification.handle_messages(Mock(), messages)

        handler.update.assert_called_with(messages)

    def test_display_passed_to_handlers_draw_method(self):
        handler = Mock()
        display = Mock()

        notification = Notification(handler)
        notification.handle_messages(display, [])

        handler.draw.assert_called_with(display)


if __name__ == '__main__':
    unittest.main()
