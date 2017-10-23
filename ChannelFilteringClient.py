class ChannelFilteringClient:
    channel = None

    def __init__(self, client, channel_name):
        self.client = client
        self.channel_name = channel_name

    def connect(self):
        return self.client.rtm_connect(with_team_state=False)

    def read_messages(self, only_latest=False):
        if not self.channel:
            self.channel = self._find_channel(self.channel_name)

            if not self.channel:
                raise ValueError("Failed to find channel '%s'. Have you created the channel?" % self.channel_name)

        messages = self._find_dashboard_messages(self.client.rtm_read())

        if only_latest and messages:
            return [messages[-1]]

        return messages

    def _find_channel(self, channel_name):
        channel_list = self.client.api_call("channels.list", exclude_archived=1)
        return next(iter([c for c in channel_list['channels'] if c['name'] == channel_name]), None)

    def _find_dashboard_messages(self, events):
        messages = [e for e in events if e['type'] == 'message']
        return [m for m in messages if m['channel'] == self.channel['id']]
