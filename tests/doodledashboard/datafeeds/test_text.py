import unittest

from doodledashboard.configuration.config import DashboardConfigReader
from doodledashboard.datafeeds.text import TextFeed, TextFeedSection


class TestCliStart(unittest.TestCase):
    _SINGLE_OUTPUT_YAML_CONFIG = """
        data-feeds:
          - source: text
            text: Hello World
    """

    _MULTI_OUTPUT_YAML_CONFIG = """
        data-feeds:
          - source: text
            text:
              - Hello
              - World
    """

    def test_feed_is_created_from_single_text_in_configuration(self):
        config_reader = DashboardConfigReader()
        config_reader.add_data_feed_creators([TextFeedSection()])

        dashboard = config_reader.read_yaml(TestCliStart._SINGLE_OUTPUT_YAML_CONFIG)

        data_feeds = dashboard.get_data_feeds()
        self.assertEqual(1, len(data_feeds))
        self.assertIsInstance(data_feeds[0], TextFeed)
        self.assertEqual(["Hello World"], data_feeds[0].get_text())

    def test_feed_is_created_from_multi_text_in_configuration(self):
        config_reader = DashboardConfigReader()
        config_reader.add_data_feed_creators([TextFeedSection()])

        dashboard = config_reader.read_yaml(TestCliStart._MULTI_OUTPUT_YAML_CONFIG)

        data_feeds = dashboard.get_data_feeds()
        self.assertEqual(1, len(data_feeds))
        self.assertIsInstance(data_feeds[0], TextFeed)
        self.assertEqual(["Hello", "World"], data_feeds[0].get_text())

    def test_feed_returns_single_data_entries(self):
        entities = TextFeed("Hello World").get_latest_entities()

        self.assertEqual(1, len(entities), "Returns one textual entity per poll")

        entity = entities[0]
        self.assertEqual("Hello World", entity.get_text())

    def test_feed_returns_multiple_data_entries(self):
        entities = TextFeed(["Hello", "World"]).get_latest_entities()

        self.assertEqual(2, len(entities), "Returns two textual entities per poll")

        self.assertEqual("Hello", entities[0].get_text())
        self.assertEqual("World", entities[1].get_text())


if __name__ == "__main__":
    unittest.main()
