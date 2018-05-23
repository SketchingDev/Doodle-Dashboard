import unittest
from doodledashboard.configuration.config import DashboardConfigReader
from doodledashboard.datafeeds.datetime import DateTimeFeedSection, DateTimeFeed


class TestCliStart(unittest.TestCase):
    _YAML_CONFIG = """
        data-feeds:
          - source: datetime
    """

    def test_feed_is_created_from_configuration(self):
        config_reader = DashboardConfigReader()
        config_reader.add_data_feed_creators([DateTimeFeedSection()])

        dashboard = config_reader.read_yaml(TestCliStart._YAML_CONFIG)

        data_feeds = dashboard.get_data_feeds()
        self.assertEqual(1, len(data_feeds))
        self.assertIsInstance(data_feeds[0], DateTimeFeed)

    def test_feed_returns_date_and_time(self):
        entities = DateTimeFeed().get_latest_entities()

        self.assertEqual(1, len(entities), "Returns one textual entity per poll")

        entity = entities[0]
        self.assertRegex(entity.get_text(), "\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "Textual data matches date/time pattern")


if __name__ == "__main__":
    unittest.main()
