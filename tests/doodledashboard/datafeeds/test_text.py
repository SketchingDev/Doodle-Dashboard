import unittest

from doodledashboard.datafeeds.text import TextFeed, TextFeedConfig


class TestCliStart(unittest.TestCase):

    def test_section_creates_for_text(self):
        config = {
            "source": "text"
        }
        self.assertTrue(TextFeedConfig().can_create(config))

    def test_section_does_not_create_for_other(self):
        config = {
            "source": "other"
        }
        self.assertFalse(TextFeedConfig().can_create(config))

    def test_section_creates_text_data_feed(self):
        config = {
            "source": "text",
            "text": "Hello World"
        }

        data_feed = TextFeedConfig().create(config)

        self.assertIsInstance(data_feed, TextFeed)

    def test_text_data_feed_returns_single_message(self):
        config = {
            "source": "text",
            "text": "Hello World"
        }

        data_feed = TextFeedConfig().create(config)
        entities = data_feed.get_latest_messages()

        self.assertEqual(1, len(entities))
        self.assertEqual("Hello World", entities[0].get_text())

    def test_text_data_feed_returns_multiple_messages(self):
        config = {
            "source": "text",
            "text": ["Hello", "World"]
        }

        data_feed = TextFeedConfig().create(config)
        entities = data_feed.get_latest_messages()

        self.assertEqual(2, len(entities))
        self.assertEqual("Hello", entities[0].get_text())
        self.assertEqual("World", entities[1].get_text())


if __name__ == "__main__":
    unittest.main()
