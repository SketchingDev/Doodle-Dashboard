import unittest
from mock import Mock, mock

from doodledashboard.dashboard_runner import DashboardRunner, Dashboard
from doodledashboard.datafeeds.datafeed import TextEntity


@mock.patch("time.sleep")
class TestDashboardRunner(unittest.TestCase):

    def test_entities_from_data_feeds_are_passed_to_notification(self, time_sleep):
        entity_1 = TextEntity('')
        entity_2 = TextEntity('')
        entity_3 = TextEntity('')

        data_feeds = [Mock(), Mock()]
        data_feeds[0].get_latest_entities.return_value = [entity_1, entity_2]
        data_feeds[1].get_latest_entities.return_value = [entity_3]

        notification = Mock()

        dashboard = Dashboard(0, Mock(), data_feeds, [notification])

        DashboardRunner(dashboard).cycle()

        notification.process.assert_called_once_with([entity_1, entity_2, entity_3])

    def test_display_is_passed_to_notification(self, time_sleep):
        display = Mock()
        notification = Mock()

        dashboard = Dashboard(0, display, [], [notification])
        DashboardRunner(dashboard).cycle()

        notification.draw.assert_called_once_with(display)

    def test_get_get_latest_entities_called_for_all_data_feeds_when_cycle_called(self, time_sleep):
        data_feeds = [self._create_emtpy_data_feed(),
                      self._create_emtpy_data_feed()]

        dashboard = Dashboard(0, Mock(), data_feeds, [Mock()])
        DashboardRunner(dashboard).cycle()

        data_feeds[0].get_latest_entities.assert_called()
        data_feeds[1].get_latest_entities.assert_called()

    @staticmethod
    def _create_emtpy_data_feed():
        data_feed = Mock()
        data_feed.get_latest_entities.return_value = []
        return data_feed


if __name__ == "__main__":
    unittest.main()
