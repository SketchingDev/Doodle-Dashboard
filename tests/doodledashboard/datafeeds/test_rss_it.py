import unittest
import pytest
from doodledashboard.datafeeds.rss import RssFeed
from pytest_localserver import http


@pytest.mark.usefixtures
class TestRssFeedIT(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_real_rss_feed_parsed(self):
        feed = \
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

        self.http_server.serve_content(feed)

        repo = RssFeed(self.http_server.url)
        messages = repo.get_latest_entities()

        self.assertEqual(2, len(messages))
        self.assertMultiLineEqual("Dummy Item 1\nhttps://dummy-link/1\nDesc for 1", messages[0].get_text())
        self.assertMultiLineEqual("Dummy Item 2\nhttps://dummy-link/2", messages[1].get_text())


if __name__ == "__main__":
    unittest.main()
