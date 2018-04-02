import unittest

import yaml

from doodledashboard.config import DashboardConfig
from doodledashboard.datafeeds.repository import MessageModel
from doodledashboard.datafeeds.rss import RssFeedConfigCreator, RssFeed
from doodledashboard.displays.loggingdisplay import LoggingDisplayConfigCreator, LoggingDisplay
from doodledashboard.filters import MessageContainsTextFilterCreator, MessageMatchesRegexTextFilterCreator
from doodledashboard.handlers.weather.weather import WeatherMessageHandlerConfigCreator


class TestYamlConfigurationIT(unittest.TestCase):

    _VALID_YAML_CONFIG = '''
        interval: 20
        display: logging
        
        data-feeds:
          - source: rss
            url: http://example-weather.com/feed.rss
        
        notifications:
          - title: Local weather
            handler: weather-handler
            filter-chain:
              - description: Keep messages about the weather
                type: message-contains-text
                text: weather
              - description: Keep messages with forecast
                type: message-matches-regex
                pattern: (rain|sun|snow)
                
    '''

    def test_interval_read_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        self.assertEqual(20, dashboard_config.get_interval())

    def test_display_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_display_creator(LoggingDisplayConfigCreator())

        display = dashboard_config.get_display()
        self.assertIsInstance(display, LoggingDisplay)

    def test_data_source_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_data_source_creators(RssFeedConfigCreator())

        data_sources = dashboard_config.get_data_feeds()
        self.assertEqual(1, len(data_sources))

        self.assertIsInstance(data_sources[0], RssFeed)
        self.assertEqual('http://example-weather.com/feed.rss', data_sources[0].get_url())

    def test_notifications_with_handler_and_filters_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_handler_creators(WeatherMessageHandlerConfigCreator({}))
        dashboard_config.set_filter_creators(MessageContainsTextFilterCreator())

        notifications = dashboard_config.get_notifications()
        self.assertEqual(1, len(notifications))

    def test_notifications_with_handler_and_no_filters_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_handler_creators(WeatherMessageHandlerConfigCreator({}))

        notifications = dashboard_config.get_notifications()
        self.assertEqual(1, len(notifications))

    def test_notifications_with_handler_and_with_filters_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_handler_creators(WeatherMessageHandlerConfigCreator({}))

        filter_creators_chain = MessageContainsTextFilterCreator()
        filter_creators_chain.add(MessageMatchesRegexTextFilterCreator())
        dashboard_config.set_filter_creators(filter_creators_chain)

        notifications = dashboard_config.get_notifications()

        self.assertEqual(1, len(notifications))

        messages = notifications[0]\
            .get_filter_chain()\
            .filter([MessageModel("weather sun"), MessageModel("weather spoons"), MessageModel("test")])

        self.assertEqual(1, len(messages))
        self.assertEqual("weather sun", messages[0].get_text())


if __name__ == '__main__':
    unittest.main()
