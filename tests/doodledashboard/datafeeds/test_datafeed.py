import unittest

from doodledashboard.datafeeds.datafeed import DataFeed, Message


class DummyFeed(DataFeed):

    def get_latest_messages(self):
        return [Message("dummy message")]


class TestDataFeed(unittest.TestCase):

    def test_data_feed_name_set_against_messages(self):
        dummy_feed = DummyFeed()

        dummy_feed.name = "dummy-feed"
        messages = dummy_feed.get_messages()

        self.assertEqual("dummy-feed", messages[0].source_name)


if __name__ == "__main__":
    unittest.main()
