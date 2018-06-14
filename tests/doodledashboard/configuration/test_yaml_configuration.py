import unittest
from sketchingdev.custom import ConsoleDisplay

from doodledashboard.configuration.config import DashboardConfigReader, FilterConfigSection
from doodledashboard.datafeeds.rss import RssFeedSection, RssFeed
from doodledashboard.filters.filter import TextEntityFilter
from doodledashboard.handlers.handler import MessageHandlerConfigSection


class TestYamlConfigurationIT(unittest.TestCase):
    _VALID_YAML_CONFIG = """
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
    """

    def test_interval_read_from_yaml(self):
        config_reader = DashboardConfigReader()
        config_reader.add_available_displays([ConsoleDisplay])
        dashboard = config_reader.read_yaml(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        self.assertEqual(20, dashboard.get_interval())

    def test_display_created_from_yaml(self):
        config_reader = DashboardConfigReader()
        config_reader.add_available_displays([ConsoleDisplay])
        dashboard = config_reader.read_yaml(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        self.assertIsInstance(dashboard.get_display(), ConsoleDisplay)

    def test_data_source_created_from_yaml(self):
        config_reader = DashboardConfigReader()
        config_reader.add_available_displays([ConsoleDisplay])
        config_reader.add_data_feed_creators([RssFeedSection()])

        dashboard = config_reader.read_yaml(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        data_feeds = dashboard.get_data_feeds()
        self.assertEqual(1, len(data_feeds))

        self.assertIsInstance(data_feeds[0], RssFeed)
        self.assertEqual("http://example-image.com/feed.rss", data_feeds[0].get_url())

    def test_notifications_with_handler_and_filters_created_from_yaml(self):
        filter_creator = DummyFilterCreator()

        config_reader = DashboardConfigReader()
        config_reader.add_available_displays([ConsoleDisplay])
        config_reader.add_handler_creators([DummyHandlerConfigCreator({})])
        config_reader.add_filter_creators([filter_creator])

        dashboard = config_reader.read_yaml(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        notifications = dashboard.get_notifications()
        self.assertEqual(1, len(notifications))

        configs = filter_creator.get_configs()
        self.assertEqual(2, len(configs))
        self.assertEqual("Test filter 1", configs[0]["description"])
        self.assertEqual("Test filter 2", configs[1]["description"])

    def test_notifications_with_handler_and_no_filters_created_from_yaml(self):
        config_reader = DashboardConfigReader()

        handlerCreator = DummyHandlerConfigCreator({})
        config_reader.add_available_displays([ConsoleDisplay])
        config_reader.add_handler_creators([handlerCreator])

        dashboard = config_reader.read_yaml(TestYamlConfigurationIT._VALID_YAML_CONFIG)

        notifications = dashboard.get_notifications()
        self.assertEqual(1, len(notifications))

        configs = handlerCreator.get_configs()
        self.assertEqual(1, len(configs))
        self.assertEqual("Hello World", configs[0]["text"])


class DummyHandlerConfigCreator(MessageHandlerConfigSection):
    _DUMMY_HANDLER = True

    def __init__(self, key_value_storage):
        MessageHandlerConfigSection.__init__(self, key_value_storage)
        self._configs_passed_in = []

    def creates_for_id(self, filter_id):
        return True

    def create_handler(self, config_section, key_value_store):
        self._configs_passed_in.append(config_section)
        return DummyHandlerConfigCreator._DUMMY_HANDLER

    def get_configs(self):
        return self._configs_passed_in


class DummyFilterCreator(FilterConfigSection):
    _DUMMY_FILTER = TextEntityFilter()

    def __init__(self):
        FilterConfigSection.__init__(self)
        self._configs_passed_in = []

    def creates_for_id(self, filter_id):
        return True

    def create_item(self, config_section):
        self._configs_passed_in.append(config_section)
        return DummyFilterCreator._DUMMY_FILTER

    def get_configs(self):
        return self._configs_passed_in


if __name__ == "__main__":
    unittest.main()
