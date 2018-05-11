import unittest

from mock import Mock, mock

from doodledashboard.dashboard_runner import DashboardRunner, Dashboard


@mock.patch("time.sleep")
@mock.patch("itertools.cycle", side_effect=(lambda values: values))
class TestDashboardRunner(unittest.TestCase):

    def test_messages_from_data_feeds_are_passed_to_notification(self, time_sleep, itertools_cycle):
        message_1 = Mock()
        message_2 = Mock()
        message_3 = Mock()

        data_feeds = [Mock(), Mock()]
        data_feeds[0].get_latest_messages.return_value = [message_1, message_2]
        data_feeds[1].get_latest_messages.return_value = [message_3]

        notification = Mock()

        dashboard = Dashboard(0, Mock(), data_feeds, [notification])

        DashboardRunner(dashboard).run()

        notification.handle_messages.assert_called_once_with(mock.ANY, [message_1, message_2, message_3])

    def test_display_is_passed_to_notification(self, time_sleep, itertools_cycle):
        display = Mock()
        data_feed = Mock()

        dashboard = Dashboard(0, display, [], [data_feed])
        DashboardRunner(dashboard).run()

        data_feed.handle_messages.assert_called_once_with(display, mock.ANY)

    def test_get_latest_messages_not_run_on_data_feeds_when_no_notifications_given(self, time_sleep, itertools_cycle):
        data_feeds = [self._create_emtpy_data_feed()]

        dashboard = Dashboard(0, Mock(), data_feeds, [])
        DashboardRunner(dashboard).run()

        data_feeds[0].get_latest_messages.assert_not_called()

    def test_get_latest_messages_called_for_all_data_feeds_when_start_called(self, time_sleep, itertools_cycle):
        data_feeds = [self._create_emtpy_data_feed(),
                      self._create_emtpy_data_feed()]

        dashboard = Dashboard(0, Mock(), data_feeds, [Mock()])
        DashboardRunner(dashboard).run()

        data_feeds[0].get_latest_messages.assert_called()
        data_feeds[1].get_latest_messages.assert_called()

    @staticmethod
    def _create_emtpy_data_feed():
        data_feed = Mock()
        data_feed.get_latest_messages.return_value = []
        return data_feed


if __name__ == "__main__":
    unittest.main()
