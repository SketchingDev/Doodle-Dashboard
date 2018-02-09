import logging
import shelve
import sys

import yaml

from doodledashboard.config import RootCreator, DashboardConfig
from doodledashboard.dashboard import Dashboard
from doodledashboard.datasources.rss import RssRepositoryConfigCreator
from doodledashboard.datasources.slack import SlackRepositoryConfigCreator
from doodledashboard.displays.display import LoggingDisplayConfigCreator
from doodledashboard.filters import MessageMatchesRegexTextFilterCreator, MessageContainsTextFilterCreator
from doodledashboard.handlers.weather.weather import WeatherMessageHandlerConfigCreator


def register_logger(logger):
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)


def get_display_creators():
    creator = RootCreator()
    creator.add(LoggingDisplayConfigCreator())

    return creator

def get_data_source_creators():
    creator = RootCreator()
    creator.add(RssRepositoryConfigCreator())
    creator.add(SlackRepositoryConfigCreator())

    return creator


def get_handler_creators(key_value_store):
    creator = RootCreator()
    creator.add(WeatherMessageHandlerConfigCreator(key_value_store))

    return creator


def get_filter_creators():
    creator = RootCreator()
    creator.add(MessageMatchesRegexTextFilterCreator())
    creator.add(MessageContainsTextFilterCreator())

    return creator


def start():
    _logger = logging.getLogger('doodle_dashboard')
    register_logger(_logger)

    _shelve = shelve.open('/tmp/shelve')

    # _config = yaml.load(file(sys.argv[1], 'r'))
    # _config = yaml.safe_load()

    _config = None
    with open(sys.argv[1], 'r') as stream:
        _config = yaml.load(stream)

    dashboard_config = DashboardConfig(_config)
    dashboard_config.set_display_creator(get_display_creators())
    dashboard_config.set_data_source_creators(get_data_source_creators())
    dashboard_config.set_handler_creators(get_handler_creators(_shelve))
    dashboard_config.set_filter_creators(get_filter_creators())

    _dashboard = Dashboard(
        dashboard_config.get_display(),
        dashboard_config.get_data_sources(),
        dashboard_config.get_notifications()
    )
    _dashboard.set_update_interval(dashboard_config.get_interval())

    try:
        _dashboard.start()
    except KeyboardInterrupt:
        _shelve.close()
        sys.exit(0)
    except ValueError as err:
        _shelve.close()
        _logger.critical(err)
        sys.exit(1)


if __name__ == '__main__':
    start()
