import logging
from requests import ConnectionError
from slackclient import SlackClient

from doodledashboard.configuration.config import MissingRequiredOptionException, ConfigSection
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class SlackFeed(DataFeed):
    _channel = None

    def __init__(self, client, channel_name):
        DataFeed.__init__(self)
        self._client = client
        self._channel_name = channel_name
        self._logger = logging.getLogger("doodledashboard.SlackRepository")
        self._connected = False
        self._connected_previously = False

    def get_latest_messages(self):
        if not self._connected:
            self._connected = self._try_connect()

        if not self._test_connection():
            self._logger.info("Failed to connect to Slack, will try again next time around")
            self._connected = False
            return []

        if not self._channel:
            self._channel = self._try_find_channel(self._channel_name)

        events = self._client.rtm_read()
        self._logger.info("Events from Slack: %s" % events)

        if len(events) is 1 and events[0]["type"] == "hello":
            self._logger.info("Slack connection confirmed with hello: %s" % events)
            events = self._client.rtm_read()
            self._logger.info("Events from Slack: %s" % events)

        events = SlackFeed._filter_events_by_channel(self._channel, events)
        events = SlackFeed._filter_events_by_type(events, "message")
        events = SlackFeed._filter_events_with_text(events)

        return [Message(event["text"], self) for event in events]

    def _test_connection(self):
        connected = False
        try:
            response = self._client.api_call("api.test")
            if response["ok"]:
                connected = True
            else:
                self._logger.info("Slack threw the error '%s'" % response['error'])
        except ConnectionError:
            connected = False
        return connected

    def _try_connect(self):
        connected = self._client.rtm_connect(with_team_state=False)
        if connected:
            self._logger.info("Connected to Slack. Huzzah!")
            self._connected_previously = True
        else:
            if self._connected_previously:
                message = "Failed to connect to Slack. I've connected before so likely the internet is just down."
            else:
                message = "Failed to connect to Slack. Is the Slack token correct?"

            self._logger.info(message)

        return connected

    def _try_find_channel(self, channel_name):
        channel = None
        try:
            channel = self._find_channel(channel_name)
            if not channel:
                self._logger.info(
                    "Failed to find Slack channel '%s'. Have you provided created it?" % self._channel_name)
        except ConnectionError:
            pass

        return channel

    def _find_channel(self, channel_name):
        channel_list = self._client.api_call("channels.list", exclude_archived=1)
        return next(iter([c for c in channel_list["channels"] if c["name"] == channel_name]), None)

    def __str__(self):
        return "Slack feed for %s channel" % self._channel_name

    @staticmethod
    def _filter_events_with_text(events):
        return [e for e in events if "text" in e]

    @staticmethod
    def _filter_events_by_type(events, type):
        return [e for e in events if e["type"] == type]

    @staticmethod
    def _filter_events_by_channel(channel, events):
        return [e for e in events if "channel" in e and e["channel"] == channel["id"]]

    @staticmethod
    def get_config_factory():
        return SlackFeedConfig()


class SlackFeedConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "source", "slack"

    def create(self, config_section):
        if "token" not in config_section:
            raise MissingRequiredOptionException("Expected 'token' option to exist")

        if "channel" not in config_section:
            raise MissingRequiredOptionException("Expected 'channel' option to exist")

        slack_client = SlackClient(config_section["token"])
        channel = config_section["channel"]
        return SlackFeed(slack_client, channel)
