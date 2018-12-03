import pytest
import unittest
from doodledashboard.component import MissingRequiredOptionException
from pytest_localserver import http

from doodledashboard.datafeeds.rss import RssFeed, RssFeedConfig


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}
    _VALID_URL = "https://sketchingdev.co.uk/feed.xml"

    def test_id_is_rss(self):
        self.assertEqual("rss", RssFeedConfig.get_id())

    def test_exception_raised_when_no_url_in_options(self):
        with pytest.raises(MissingRequiredOptionException) as err_info:
            RssFeedConfig().create(self._EMPTY_OPTIONS)

        self.assertEqual("Expected 'url' option to exist", err_info.value.value)

    def test_data_feed_created_with_url_from_options(self):
        options_with_url = {
            "url": "https://sketchingdev.co.uk/feed.xml"
        }

        data_feed = RssFeedConfig().create(options_with_url)

        self.assertIsInstance(data_feed, RssFeed)

    def test_exception_raised_when_invalid_sort_in_options(self):
        options_with_invalid_sort = {
            "url": self._VALID_URL,
            "sort": "invalid"
        }

        with pytest.raises(MissingRequiredOptionException) as err_info:
            RssFeedConfig().create(options_with_invalid_sort)

        self.assertEqual("Sorting value for RSS feed can only be either ascending or descending", err_info.value.value)

    def test_data_feed_created_with_ascending_sort_order_from_options(self):
        options_with_ascending_order = {
            "url": self._VALID_URL,
            "sort": "newest"
        }

        data_feed = RssFeedConfig().create(options_with_ascending_order)
        self.assertEqual("newest", data_feed.get_sort_order())

    def test_data_feed_created_with_descending_sort_order_from_options(self):
        options_with_descending_order = {
            "url": self._VALID_URL,
            "sort": "oldest"
        }

        data_feed = RssFeedConfig().create(options_with_descending_order)
        self.assertEqual("oldest", data_feed.get_sort_order())


@pytest.mark.usefixtures
class TestFeed(unittest.TestCase):
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

    def test_messages_ordered_by_date_ascending(self):
        self.http_server.serve_content(TestFeed._RSS_FEED)
        options = {
            "url": self.http_server.url,
            "sort": "oldest"
        }

        data_feed = RssFeedConfig().create(options)
        messages = data_feed.get_latest_messages()

        self.assertEqual(3, len(messages))
        self.assertEqual("Dummy Item 1\nhttps://item/1\n2018-01-01T00:00:00+00:00", messages[0].text)
        self.assertEqual("Dummy Item 3\nhttps://item/3\n2018-01-02T00:00:00+00:00", messages[1].text)
        self.assertEqual("Dummy Item 2\nhttps://item/2\n2018-01-03T00:00:00+00:00", messages[2].text)

    def test_messages_ordered_by_date_descending(self):
        self.http_server.serve_content(TestFeed._RSS_FEED)
        options = {
            "url": self.http_server.url,
            "sort": "newest"
        }

        data_feed = RssFeedConfig().create(options)
        messages = data_feed.get_latest_messages()

        self.assertEqual(3, len(messages))
        self.assertEqual("Dummy Item 2\nhttps://item/2\n2018-01-03T00:00:00+00:00", messages[0].text)
        self.assertEqual("Dummy Item 3\nhttps://item/3\n2018-01-02T00:00:00+00:00", messages[1].text)
        self.assertEqual("Dummy Item 1\nhttps://item/1\n2018-01-01T00:00:00+00:00", messages[2].text)

    def test_messages_sorted_natural_order_by_default(self):
        self.http_server.serve_content(TestFeed._RSS_FEED)
        options = {
            "url": self.http_server.url
        }

        data_feed = RssFeedConfig().create(options)
        messages = data_feed.get_latest_messages()

        self.assertEqual(3, len(messages))
        self.assertEqual("Dummy Item 1\nhttps://item/1\n2018-01-01T00:00:00+00:00", messages[0].text)
        self.assertEqual("Dummy Item 2\nhttps://item/2\n2018-01-03T00:00:00+00:00", messages[1].text)
        self.assertEqual("Dummy Item 3\nhttps://item/3\n2018-01-02T00:00:00+00:00", messages[2].text)


if __name__ == "__main__":
    unittest.main()
