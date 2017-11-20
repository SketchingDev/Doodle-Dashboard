import logging


class MessageModel:
    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text


class Repository:
    def __init__(self):
        pass

    def get_latest_messages(self):
        raise NotImplementedError('Implement this method')


class SlackRepository(Repository):
    channel = None

    def __init__(self, client, channel_name):
        Repository.__init__(self)
        self._client = client
        self._channel_name = channel_name
        self._logger = logging.getLogger('raspberry_pi_dashboard.SlackRepository')
        self._connected_previously = False

    def _connect(self):
        return self._client.rtm_connect(with_team_state=False)

    def get_latest_messages(self):
        if not self._connect():
            if self._connected_previously:
                message = 'Failed to connect to Slack. I\'ve connected before so likely the internet is just down.'
            else:
                message = 'Failed to connect to Slack. Is the Slack token correct?'

            self._logger.info(message)
            return []
        else:
            self._connected_previously = True

            if not self.channel:
                self.channel = self._find_channel(self._channel_name)

                if not self.channel:
                    self._logger.info("Failed to find Slack channel '%s'. Have you provided created it?" % self._channel_name)

            events = self._client.rtm_read()
            logging.info(events)
            events = SlackRepository._filter_events_by_channel(self.channel, events)
            events = SlackRepository._filter_events_by_type(events, 'message')
            events = SlackRepository._filter_events_with_text(events)

            return [MessageModel(event['text']) for event in events]

    def _find_channel(self, channel_name):
        channel_list = self._client.api_call("channels.list", exclude_archived=1)
        return next(iter([c for c in channel_list['channels'] if c['name'] == channel_name]), None)

    @staticmethod
    def _filter_events_with_text(events):
        return [e for e in events if 'text' in e]

    @staticmethod
    def _filter_events_by_type(events, type):
        return [e for e in events if e['type'] == type]

    @staticmethod
    def _filter_events_by_channel(channel, events):
        return [e for e in events if 'channel' in e and e['channel'] == channel['id']]