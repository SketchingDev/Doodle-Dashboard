import pytest
import unittest
from pytest_localserver import http

from doodledashboard.configuration.config import DashboardConfigReader
from doodledashboard.datafeeds.rss import RssFeed, RssFeedSection


@pytest.mark.usefixtures
class TestRssFeed(unittest.TestCase):
    _YAML_CONFIG = """
        data-feeds:
          - source: rss
            url: https://sketchingdev.co.uk/feed.xml
    """

    _RSS_FEED = \
        '<?xml version="1.0" encoding="UTF-8"?>\
        <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\
          <channel>\
            <title>Example RSS Feed</title>\
            <link>https://exmaple/rss/feed/</link>\
            <description>Example RSS feed used for tests</description>\
            <item>\
              <title>Dummy Item 1</title>\
              <link>https://dummy-link/1</link>\
              <description>Desc for 1</description>\
            </item>\
            <item>\
              <title>Dummy Item 2</title>\
              <link>https://dummy-link/2</link>\
            </item>\
          </channel>\
        </rss>'

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_feed_is_created_from_configuration(self):
        config_reader = DashboardConfigReader()
        config_reader.add_data_feed_creators([RssFeedSection()])

        dashboard = config_reader.read_yaml(TestRssFeed._YAML_CONFIG)

        data_feeds = dashboard.get_data_feeds()
        self.assertEqual(1, len(data_feeds))
        self.assertIsInstance(data_feeds[0], RssFeed)
        self.assertEqual("https://sketchingdev.co.uk/feed.xml", data_feeds[0].get_url())

    def test_real_rss_feed_parsed(self):
        self.http_server.serve_content(TestRssFeed._RSS_FEED)

        repo = RssFeed(self.http_server.url)
        messages = repo.get_latest_entities()

        self.assertEqual(2, len(messages))
        self.assertMultiLineEqual("Dummy Item 1\nhttps://dummy-link/1\nDesc for 1", messages[0].get_text())
        self.assertMultiLineEqual("Dummy Item 2\nhttps://dummy-link/2", messages[1].get_text())


if __name__ == "__main__":
    unittest.main()
