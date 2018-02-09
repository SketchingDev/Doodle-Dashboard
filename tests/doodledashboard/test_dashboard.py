import unittest

from mock import Mock, mock

from doodledashboard.dashboard import Dashboard


@mock.patch('time.sleep')
@mock.patch('itertools.cycle', side_effect=(lambda values: values))
class TestDashboard(unittest.TestCase):

    def test_messages_from_repositories_are_passed_to_notification(self, time_sleep, itertools_cycle):
        message_1 = Mock()
        message_2 = Mock()
        message_3 = Mock()

        repositories = [Mock(), Mock()]
        repositories[0].get_latest_messages.return_value = [message_1, message_2]
        repositories[1].get_latest_messages.return_value = [message_3]

        notification = Mock()

        Dashboard(Mock(), repositories, [notification]).start()

        notification.handle_messages.assert_called_once_with(mock.ANY, [message_1, message_2, message_3])

    def test_display_is_passed_to_notification(self, time_sleep, itertools_cycle):
        display = Mock()
        notification = Mock()

        Dashboard(display, [], [notification]).start()

        notification.handle_messages.assert_called_once_with(display, mock.ANY)

    def test_get_latest_messages_not_run_on_repositories_when_no_notifications_given(self, time_sleep, itertools_cycle):
        repositories = [self._create_emtpy_repository()]

        Dashboard(Mock(), repositories, []).start()

        repositories[0].get_latest_messages.assert_not_called()

    def test_get_latest_messages_called_for_all_repositories_when_start_called(self, time_sleep, itertools_cycle):
        repositories = [self._create_emtpy_repository(),
                        self._create_emtpy_repository()]

        Dashboard(Mock(), repositories, [Mock()]).start()

        repositories[0].get_latest_messages.assert_called()
        repositories[1].get_latest_messages.assert_called()

    @staticmethod
    def _create_emtpy_repository():
        repository = Mock()
        repository.get_latest_messages.return_value = []
        return repository


if __name__ == '__main__':
    unittest.main()
