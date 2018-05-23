import unittest

from mock import Mock, mock

from doodledashboard.dashboard_runner import DashboardRunner, Dashboard


@mock.patch("time.sleep")
@mock.patch("itertools.cycle", side_effect=(lambda values: values))
class TestDashboardRunner(unittest.TestCase):

    def test_entities_from_data_feeds_are_passed_to_notification(self, time_sleep, itertools_cycle):
        entity_1 = Mock()
        entity_2 = Mock()
        entity_3 = Mock()

        data_feeds = [Mock(), Mock()]
        data_feeds[0].get_latest_entities.return_value = [entity_1, entity_2]
        data_feeds[1].get_latest_entities.return_value = [entity_3]

        notification = Mock()

        dashboard = Dashboard(0, Mock(), data_feeds, [notification])

        DashboardRunner(dashboard).run()

        notification.handle_entities.assert_called_once_with(mock.ANY, [entity_1, entity_2, entity_3])

    def test_display_is_passed_to_notification(self, time_sleep, itertools_cycle):
        display = Mock()
        data_feed = Mock()

        dashboard = Dashboard(0, display, [], [data_feed])
        DashboardRunner(dashboard).run()

        data_feed.handle_entities.assert_called_once_with(display, mock.ANY)

    def test_get_get_latest_entities_not_run_on_data_feeds_when_no_notifications_given(
            self, time_sleep, itertools_cycle):
        data_feeds = [self._create_emtpy_data_feed()]

        dashboard = Dashboard(0, Mock(), data_feeds, [])
        DashboardRunner(dashboard).run()

        data_feeds[0].get_latest_entities.assert_not_called()

    def test_get_get_latest_entities_called_for_all_data_feeds_when_start_called(self, time_sleep, itertools_cycle):
        data_feeds = [self._create_emtpy_data_feed(),
                      self._create_emtpy_data_feed()]

        dashboard = Dashboard(0, Mock(), data_feeds, [Mock()])
        DashboardRunner(dashboard).run()

        data_feeds[0].get_latest_entities.assert_called()
        data_feeds[1].get_latest_entities.assert_called()

    @staticmethod
    def _create_emtpy_data_feed():
        data_feed = Mock()
        data_feed.get_latest_entities.return_value = []
        return data_feed


if __name__ == "__main__":
    unittest.main()
