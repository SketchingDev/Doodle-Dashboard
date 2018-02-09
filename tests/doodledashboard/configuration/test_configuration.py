import unittest

import yaml
from mock import Mock

from doodledashboard.config import RootCreator, DashboardConfig
from doodledashboard.datasources.rss import RssRepositoryConfigCreator
from doodledashboard.datasources.slack import SlackRepositoryConfigCreator
from doodledashboard.displays.display import LoggingDisplayConfigCreator
from doodledashboard.filters import MessageContainsTextFilterCreator, \
    MessageMatchesRegexTextFilterCreator
from doodledashboard.handlers.weather.weather import WeatherMessageHandlerConfigCreator


class TestFilterConfigurationIT(unittest.TestCase):

    def test_display_created_from_yaml(self):
        config = yaml.safe_load('''
            display: logging
        ''')

        creator = RootCreator()
        creator.add(LoggingDisplayConfigCreator())

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_display_creator(creator)

        self.assertIsNotNone(dashboard_config.get_display())

    def test_handlers(self):
        config = yaml.safe_load('''
            notifications:
              - title: Test weather handler 1
                handler: weather-handler
                filter-chain:
                  - description: Keep messages from RSS feeds
                    type: message-contains-text
                    text: test1
                  - description: Keep messages from RSS feeds
                    type: message-contains-text
                    text: test2
              - title: Test weather handler 2
                handler: weather-handler
                filter-chain:
                  - description: Keep messages from RSS feeds
                    type: message-contains-text
                    text: test3
        ''')

        handler_creator = RootCreator()
        handler_creator.add(WeatherMessageHandlerConfigCreator({}))

        filter_creator = RootCreator()
        filter_creator.add(MessageMatchesRegexTextFilterCreator())
        filter_creator.add(MessageContainsTextFilterCreator())

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_handler_creators(handler_creator)
        dashboard_config.set_filter_creators(filter_creator)

        notifications = dashboard_config.get_notifications()

        self.assertEqual(2, len(notifications))
        # self.assertEqual(2, len(notifications[0].get_filters()))
        # self.assertEqual(1, len(notifications[1].get_filters()))

    def test_data_sources_created_from_yaml(self):
        config = yaml.safe_load('''
            data-sources:
              - source: slack
                token: xxx
                channel: pi-dashboard
              - source: rss
                url: http://open.live.bbc.co.uk/weather/feeds/en/2643743/observations.rss
        ''')

        creator = RootCreator()
        creator.add(RssRepositoryConfigCreator())
        creator.add(SlackRepositoryConfigCreator())

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_data_source_creators(creator)

        data_sources = dashboard_config.get_data_sources()

        self.assertEqual(2, len(data_sources))

    def test_abc(self):
        config = yaml.safe_load('''
          - description: Keep messages containing 'testing' 
            type: message-contains-text
            text: 1
        ''')

        creator = RootCreator()
        creator.add(MessageMatchesRegexTextFilterCreator())
        creator.add(MessageContainsTextFilterCreator())

        messages = [
            TestFilterConfigurationIT.create_mock_message_with_text('testing1'),
            TestFilterConfigurationIT.create_mock_message_with_text('testing2'),
        ]

        filter = creator.create(config[0])
        self.assertIsNotNone(filter)

        filtered_messages = filter.filter(messages)
        self.assertEqual(1, len(filtered_messages))
        self.assertEqual('testing1', filtered_messages[0].get_text())

    def test_real_rss_feed_parsed(self):
        config = yaml.safe_load('''
        filter-chain:
          - description: Keep messages containing 'testing' 
            type: message-contains-text
            text: testing
          
          - description: Doesn't do anything
            type: filter-does-not-exist
            stuff: more stuff!          
          
          - description: Keep messages containing the number 1 or 3
            type: message-matches-regex
            pattern: 1|3
        ''')

        creator = RootCreator()
        creator.add(MessageContainsTextFilterCreator())
        creator.add(MessageMatchesRegexTextFilterCreator())

        messages = [
            TestFilterConfigurationIT.create_mock_message_with_text('testing1'),
            TestFilterConfigurationIT.create_mock_message_with_text('testing2'),
            TestFilterConfigurationIT.create_mock_message_with_text('test3'),
            TestFilterConfigurationIT.create_mock_message_with_text('test4'),
        ]

        filter_1 = creator.create(config['filter-chain'][0])
        filter_2 = creator.create(config['filter-chain'][1])
        filter_3 = creator.create(config['filter-chain'][2])

        self.assertIsNone(filter_2)

        filtered_messages = filter_1.filter(messages)
        self.assertEqual(2, len(filtered_messages))

        filtered_messages = filter_3.filter(filtered_messages)
        self.assertEqual(1, len(filtered_messages))

        self.assertEqual('testing1', filtered_messages[0].get_text())

    @staticmethod
    def create_mock_message_with_text(text):
        message = Mock()
        message.get_text.return_value = text
        return message


if __name__ == '__main__':
    unittest.main()
