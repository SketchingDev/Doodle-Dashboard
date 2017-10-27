import unittest

from mock import Mock

from doodledashboard.lucas.client import ChannelFilteringClient


class TestChannelFilteringClient(unittest.TestCase):

    def test_calling_connect_calls_slack_client(self):
        mock_slack_client = Mock()

        ChannelFilteringClient(mock_slack_client, '').connect()

        mock_slack_client.rtm_connect.assert_called()

    def test_find_messages_by_text_context(self):
        pass

    def abc(self):
        mock_slack_client = Mock()
        mock_slack_client.rtm_read.return_value = [{
            'channel': 123,
            'type': 'message',
            'text': ''

        }]

    def _create_message_event(self, channel_id, text):
        return {
            'channel': channel_id,
            'type': 'message',
            'text': text
        }

    def _create_channel_info(self, name, id):
        pass


if __name__ == '__main__':
    unittest.main()
