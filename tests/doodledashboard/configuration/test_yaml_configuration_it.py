import unittest

import pytest
import yaml

from doodledashboard.configuration.config import DashboardConfig
from doodledashboard.datafeeds.rss import RssFeedConfigCreator, RssFeed
from doodledashboard.displays.consoledisplay import ConsoleDisplayConfigCreator
from doodledashboard.displays.loggingdecorator import LoggingDisplayDecorator
from doodledashboard.filters import FilterConfigCreator, MessageFilter
from doodledashboard.handlers.handler import MessageHandlerConfigCreator


@pytest.mark.usefixtures
class TestYamlConfigurationIT(unittest.TestCase):
    _VALID_YAML_CONFIG = '''
        interval: 20
        display: console
        
        data-feeds:
          - source: rss
            url: http://example-image.com/feed.rss
        
        notifications:
          - title: Dummy Handler
            handler: dummy-handler
            text: Hello World
            filter-chain:
              - description: Test filter 1
                type: dummy filter
              - description: Test filter 2
                type: dummy filter
    '''

    def test_interval_read_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        self.assertEqual(20, dashboard_config.get_interval())

    def test_display_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_display_creator(ConsoleDisplayConfigCreator())

        display = dashboard_config.get_display()
        self.assertIsInstance(display, LoggingDisplayDecorator)

    def test_data_source_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)
        dashboard_config.set_data_source_creators(RssFeedConfigCreator())

        data_sources = dashboard_config.get_data_feeds()
        self.assertEqual(1, len(data_sources))

        self.assertIsInstance(data_sources[0], RssFeed)
        self.assertEqual('http://example-image.com/feed.rss', data_sources[0].get_url())

    def test_notifications_with_handler_and_filters_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        filter_creator = DummyFilterCreator()
        dashboard_config = DashboardConfig(config)
        dashboard_config.set_handler_creators(DummyHandlerConfigCreator({}))
        dashboard_config.set_filter_creators(filter_creator)

        notifications = dashboard_config.get_notifications()
        self.assertEqual(1, len(notifications))

        configs = filter_creator.get_configs()
        self.assertEqual(2, len(configs))
        self.assertEqual('Test filter 1', configs[0]['description'])
        self.assertEqual('Test filter 2', configs[1]['description'])

    def test_notifications_with_handler_and_no_filters_created_from_yaml(self):
        config = yaml.safe_load(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        dashboard_config = DashboardConfig(config)

        handlerCreator = DummyHandlerConfigCreator({})
        dashboard_config.set_handler_creators(handlerCreator)

        notifications = dashboard_config.get_notifications()
        self.assertEqual(1, len(notifications))

        configs = handlerCreator.get_configs()
        self.assertEqual(1, len(configs))
        self.assertEqual('Hello World', configs[0]['text'])


class DummyHandlerConfigCreator(MessageHandlerConfigCreator):
    _DUMMY_HANDLER = True

    def __init__(self, key_value_storage):
        MessageHandlerConfigCreator.__init__(self, key_value_storage)
        self._configs_passed_in = []

    def creates_for_id(self, filter_id):
        return True

    def create_handler(self, config_section, key_value_store):
        self._configs_passed_in.append(config_section)
        return DummyHandlerConfigCreator._DUMMY_HANDLER

    def get_configs(self):
        return self._configs_passed_in


class DummyFilterCreator(FilterConfigCreator):
    _DUMMY_FILTER = MessageFilter()

    def __init__(self):
        FilterConfigCreator.__init__(self)
        self._configs_passed_in = []

    def creates_for_id(self, filter_id):
        return True

    def create_item(self, config_section):
        self._configs_passed_in.append(config_section)
        return DummyFilterCreator._DUMMY_FILTER

    def get_configs(self):
        return self._configs_passed_in


if __name__ == '__main__':
    unittest.main()
