import unittest

from mock import Mock, call

from doodledashboard.dashboard_runner import Notification
from doodledashboard.datafeeds.datafeed import TextEntity


class TestNotification(unittest.TestCase):

    def test_filter_chain_passed_messages(self):
        messages = [TextEntity(''), TextEntity('')]

        entity_filters = [Mock()]

        notification = Notification(Mock())
        notification.set_filters(entity_filters)

        notification.handle_entities(Mock(), messages)

        entity_filters[0].filter.assert_has_calls([call(messages[0]), call(messages[1])])

    def test_messages_from_filter_passed_handlers_update_method(self):
        messages = [TextEntity('1'), TextEntity('2')]

        entity_filters = [Mock()]
        entity_filters[0].filter.return_value = messages

        handler = Mock()

        notification = Notification(handler)
        notification.set_filters(entity_filters)
        notification.handle_entities(Mock(), messages)

        handler.update.assert_has_calls([call(messages[0]), call(messages[1])])

    def test_messages_passed_to_handlers_update_method_if_filter_chain_is_not_set(self):
        messages = [TextEntity(''), TextEntity('')]

        handler = Mock()

        notification = Notification(handler)
        notification.handle_entities(Mock(), messages)

        handler.update.assert_has_calls([call(messages[0]), call(messages[1])])

    def test_display_passed_to_handlers_draw_method(self):
        handler = Mock()
        display = Mock()

        notification = Notification(handler)
        notification.handle_entities(display, [])

        handler.draw.assert_called_with(display)


if __name__ == "__main__":
    unittest.main()
