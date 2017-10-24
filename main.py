from ConfigParser import SafeConfigParser
import sys
import time

from slackclient import SlackClient

import ChannelFilteringClient
import MessageBroker
from displays import *
from handlers import *
from config import AppConfig


def main():
    config = AppConfig(SafeConfigParser())
    config.read(['defaults.cfg', sys.argv[1]])

    logger = logging.getLogger('raspberry_pi_dashboard')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    logger.addHandler(ch)

    dashboard_client = ChannelFilteringClient.ChannelFilteringClient(
        SlackClient(config.get_slack_token()),
        config.get_dashboard_channel_name()
    )

    broker = MessageBroker.MessageBroker(Display())
    broker.set_handlers([TextTagHandler()])

    if not dashboard_client.connect():
        logger.critical("Failed to connect to Slack. Connected to the internet and using the correct Slack token?")
        sys.exit(1)
    else:

        update_interval = config.get_update_interval()
        while True:
            try:
                messages = dashboard_client.read_messages(only_latest=True)
                if messages:
                    broker.process(messages[0])

            except ValueError as err:
                logging.critical(err)
                sys.exit(1)

            time.sleep(update_interval)


if __name__ == '__main__':
    main()
