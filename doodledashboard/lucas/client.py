import ConfigParser


class SlackConfig:
    def __init__(self, config):
        self._config = config

    def get_token(self):
        return self._config.get('Slack', 'Token')

    def get_channel_name(self):
        return self._config.get('Slack', 'Channel')

    @staticmethod
    def create_from_file(file_path):
        config = ConfigParser.ConfigParser()
        config.read(file_path)

        return SlackConfig(config)


class ChannelFilteringClient:
    channel = None

    def __init__(self, client, channel_name):
        self._client = client
        self._channel_name = channel_name

    def connect(self):
        return self._client.rtm_connect(with_team_state=False)

    def find_messages_by_text_content(self, text):
        if not self.channel:
            self.channel = self._find_channel(self._channel_name)

            if not self.channel:
                raise ValueError("Failed to find channel '%s'. Have you created the channel?" % self._channel_name)

        all_new_events = self._client.rtm_read()
        channel_events = self._filter_events_by_channel(self.channel, all_new_events)
        messages = self._filter_events_by_type(channel_events, 'message')
        filtered_text_messages = self._filter_events_with_text(messages)

        return self._filter_events_containing_text(filtered_text_messages, text)

    def _filter_events_containing_text(self, events, text):
        return [e for e in events if text in e['text']]

    def _find_channel(self, channel_name):
        channel_list = self._client.api_call("channels.list", exclude_archived=1)
        return next(iter([c for c in channel_list['channels'] if c['name'] == channel_name]), None)

    def _filter_events_with_text(self, events):
        return [e for e in events if 'text' in e]

    def _filter_events_by_type(self, events, type):
        return [e for e in events if e['type'] == type]

    def _filter_events_by_channel(self, channel, events):
        return [e for e in events if 'channel' in e and e['channel'] == channel['id']]
