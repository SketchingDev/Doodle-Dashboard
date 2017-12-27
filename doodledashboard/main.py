import sys

import logging
from standarddashboard import StandardDashboard
from doodledashboard.lucas.displays.display import LoggingDisplay
from lucas.config import SlackConfig

import shelve


def register_logger(logger):
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)


if __name__ == '__main__':

    _logger = logging.getLogger('doodle_dashboard')
    register_logger(_logger)

    _shelve = shelve.open('/tmp/shelve')
    _slack_config = SlackConfig.create_from_file(sys.argv[1])

    _display = LoggingDisplay()
    _dashboard = StandardDashboard(_slack_config, _display, _shelve)

    try:
        _dashboard.start()
    except KeyboardInterrupt:
        _shelve.close()
        sys.exit(0)
    except ValueError as err:
        _shelve.close()
        _logger.critical(err)
        sys.exit(1)
