import pytest
import unittest
from pytest_localserver import http

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.datafeeds.rss import RssFeed, RssFeedConfig


@pytest.mark.usefixtures
class TestRssFeed(unittest.TestCase):
    _RSS_FEED = \
        '<?xml version="1.0" encoding="UTF-8"?>\
        <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\
          <channel>\
            <title>Example RSS Feed</title>\
            <link>https://exmaple/rss/feed/</link>\
            <description>Example RSS feed used for tests</description>\
            <item>\
              <title>Dummy Item 1</title>\
              <link>https://item/1</link>\
              <updated>2018-01-01T00:00:00+00:00</updated>\
            </item>\
            <item>\
              <title>Dummy Item 2</title>\
              <link>https://item/2</link>\
              <updated>2018-01-03T00:00:00+00:00</updated>\
            </item>\
            <item>\
              <title>Dummy Item 3</title>\
              <link>https://item/3</link>\
              <updated>2018-01-02T00:00:00+00:00</updated>\
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

    def test_section_creates_for_rss(self):
        config = {
            "source": "rss"
        }
        self.assertTrue(RssFeedConfig().can_create(config))

    def test_section_does_not_create_for_other(self):
        config = {
            "source": "other"
        }
        self.assertFalse(RssFeedConfig().can_create(config))

    def test_section_throws_error_when_creating_from_config_with_no_url(self):
        config = {
            "source": "rss"
        }

        with pytest.raises(MissingRequiredOptionException) as err_info:
            RssFeedConfig().create(config)

        self.assertEqual("Expected 'url' option to exist", err_info.value.value)

    def test_section_creates_rss_data_feed(self):
        config = {
            "source": "rss",
            "url": "https://sketchingdev.co.uk/feed.xml"
        }

        data_feed = RssFeedConfig().create(config)

        self.assertIsInstance(data_feed, RssFeed)
        self.assertEqual("https://sketchingdev.co.uk/feed.xml", data_feed.get_url())
        self.assertIsNone(data_feed.get_sort_order())

    def test_section_throws_error_when_creating_from_config_with_invalid_sort(self):
        config = {
            "source": "rss",
            "url": "https://sketchingdev.co.uk/feed.xml",
            "sort": "invalid"
        }

        with pytest.raises(MissingRequiredOptionException) as err_info:
            RssFeedConfig().create(config)

        self.assertEqual("Sorting value for RSS feed can only be either ascending or descending", err_info.value.value)

    def test_section_creates_rss_data_feed_with_ascending_sort_order(self):
        config = {
            "source": "rss",
            "url": "https://example.co.uk/feed.xml",
            "sort": "newest"
        }

        data_feed = RssFeedConfig().create(config)

        self.assertIsInstance(data_feed, RssFeed)
        self.assertEqual("https://example.co.uk/feed.xml", data_feed.get_url())
        self.assertEqual("newest", data_feed.get_sort_order())

    def test_section_creates_rss_data_feed_with_descending_sort_order(self):
        config = {
            "source": "rss",
            "url": "https://sketchingdev.co.uk/feed.xml",
            "sort": "oldest"
        }

        data_feed = RssFeedConfig().create(config)

        self.assertIsInstance(data_feed, RssFeed)
        self.assertEqual("https://sketchingdev.co.uk/feed.xml", data_feed.get_url())
        self.assertEqual("oldest", data_feed.get_sort_order())

    def test_rss_ordered_by_date_ascending(self):
        self.http_server.serve_content(TestRssFeed._RSS_FEED)
        config = {
            "source": "rss",
            "url": self.http_server.url,
            "sort": "oldest"
        }

        data_feed = RssFeedConfig().create(config)
        messages = data_feed.get_latest_messages()

        self.assertEqual(3, len(messages))
        self.assertEqual("Dummy Item 1\nhttps://item/1\n2018-01-01T00:00:00+00:00", messages[0].get_text())
        self.assertEqual("Dummy Item 3\nhttps://item/3\n2018-01-02T00:00:00+00:00", messages[1].get_text())
        self.assertEqual("Dummy Item 2\nhttps://item/2\n2018-01-03T00:00:00+00:00", messages[2].get_text())

    def test_rss_ordered_by_date_descending(self):
        self.http_server.serve_content(TestRssFeed._RSS_FEED)
        config = {
            "source": "rss",
            "url": self.http_server.url,
            "sort": "newest"
        }

        data_feed = RssFeedConfig().create(config)
        messages = data_feed.get_latest_messages()

        self.assertEqual(3, len(messages))
        self.assertEqual("Dummy Item 2\nhttps://item/2\n2018-01-03T00:00:00+00:00", messages[0].get_text())
        self.assertEqual("Dummy Item 3\nhttps://item/3\n2018-01-02T00:00:00+00:00", messages[1].get_text())
        self.assertEqual("Dummy Item 1\nhttps://item/1\n2018-01-01T00:00:00+00:00", messages[2].get_text())

    def test_rss_uses_natural_order_by_default(self):
        self.http_server.serve_content(TestRssFeed._RSS_FEED)
        config = {
            "source": "rss",
            "url": self.http_server.url
        }

        data_feed = RssFeedConfig().create(config)
        messages = data_feed.get_latest_messages()

        self.assertEqual(3, len(messages))
        self.assertEqual("Dummy Item 1\nhttps://item/1\n2018-01-01T00:00:00+00:00", messages[0].get_text())
        self.assertEqual("Dummy Item 2\nhttps://item/2\n2018-01-03T00:00:00+00:00", messages[1].get_text())
        self.assertEqual("Dummy Item 3\nhttps://item/3\n2018-01-02T00:00:00+00:00", messages[2].get_text())


if __name__ == "__main__":
    unittest.main()
