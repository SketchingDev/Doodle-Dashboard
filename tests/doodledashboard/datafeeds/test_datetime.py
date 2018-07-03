import unittest

from doodledashboard.datafeeds.datetime import DateTimeFeedConfig, DateTimeFeed


class TestCliStart(unittest.TestCase):

    def test_section_creates_for_datetime(self):
        config = {
            "source": "datetime"
        }
        self.assertTrue(DateTimeFeedConfig().can_create(config))

    def test_section_does_not_create_for_other(self):
        config = {
            "source": "other"
        }
        self.assertFalse(DateTimeFeedConfig().can_create(config))

    def test_feed_is_created_from_configuration(self):
        config = {
            "source": "datetime"
        }

        data_feed = DateTimeFeedConfig().create(config)

        self.assertIsInstance(data_feed, DateTimeFeed)

    def test_feed_returns_date_and_time(self):
        config = {
            "source": "datetime"
        }

        data_feed = DateTimeFeedConfig().create(config)
        entities = data_feed.get_latest_messages()

        self.assertEqual(1, len(entities))
        self.assertRegex(entities[0].get_text(), "\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "Text matches date/time pattern")


if __name__ == "__main__":
    unittest.main()
