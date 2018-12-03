import unittest

from doodledashboard.datafeeds.datetime import DateTimeFeedConfig, DateTimeFeed


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}

    def test_id_is_datetime(self):
        self.assertEqual("datetime", DateTimeFeedConfig.get_id())

    def test_datetime_data_feed_created_with_empty_options(self):
        date_time_feed = DateTimeFeedConfig().create(self._EMPTY_OPTIONS)

        self.assertIsInstance(date_time_feed, DateTimeFeed)


class TestFeed(unittest.TestCase):
    _EMPTY_OPTIONS = {}

    def test_feed_returns_date_and_time(self):
        data_feed = DateTimeFeedConfig().create(self._EMPTY_OPTIONS)
        entities = data_feed.get_latest_messages()

        self.assertEqual(1, len(entities))
        self.assertRegex(entities[0].text, "\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "Text matches date/time pattern")


if __name__ == "__main__":
    unittest.main()
