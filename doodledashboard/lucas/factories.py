import logging

from slackclient import SlackClient

from client import ChannelFilteringClient


class DashboardLogger:
    def __init__(self):
        pass

    def register(self):
        logger = logging.getLogger('raspberry_pi_dashboard')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        return logger


class ClientFactory:
    def __init__(self):
        pass

    def create(self, config):
        slack_client = SlackClient(config.get_token())
        channel = config.get_channel_name()

        return ChannelFilteringClient(slack_client, channel)
