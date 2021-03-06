import pytest
import unittest
from doodledashboard.component import MissingRequiredOptionException

from doodledashboard.datafeeds.text import TextFeed, TextFeedCreator


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}
    _EMPTY_SECRET_STORE = {}

    def test_id_is_datetime(self):
        self.assertEqual("text", TextFeedCreator.get_id())

    def test_exception_raised_when_no_text_in_options(self):
        with pytest.raises(MissingRequiredOptionException) as err_info:
            TextFeedCreator().create(self._EMPTY_OPTIONS, self._EMPTY_SECRET_STORE)

        self.assertEqual("Expected 'text' option to exist", err_info.value.message)

    def test_data_feed_created_with_text_from_options(self):
        options_with_text = {
            "text": "Testing Testing 123"
        }

        data_feed = TextFeedCreator().create(options_with_text, self._EMPTY_SECRET_STORE)

        self.assertIsInstance(data_feed, TextFeed)

        texts = data_feed.text
        self.assertEqual(1, len(texts))
        self.assertEqual("Testing Testing 123", texts[0])

    def test_data_feed_created_with_multiple_text_from_options(self):
        options_with_multiple_text = {
            "text": ["Testing", "456"]
        }

        data_feed = TextFeedCreator().create(options_with_multiple_text, self._EMPTY_SECRET_STORE)

        self.assertIsInstance(data_feed, TextFeed)

        texts = data_feed.text
        self.assertEqual(2, len(texts))
        self.assertEqual(["Testing", "456"], texts)


class TestFeed(unittest.TestCase):
    _EMPTY_SECRET_STORE = {}

    def test_message_contains_text_from_options(self):
        options_with_text = {
            "text": "Hello World"
        }

        data_feed = TextFeedCreator().create(options_with_text, self._EMPTY_SECRET_STORE)

        messages = data_feed.get_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual("Hello World", messages[0].text)

    def test_messages_contain_text_from_options(self):
        options_with_multiple_text = {
            "text": ["Hello", "World"]
        }

        data_feed = TextFeedCreator().create(options_with_multiple_text, self._EMPTY_SECRET_STORE)

        messages = data_feed.get_messages()
        self.assertEqual(2, len(messages))
        self.assertEqual("Hello", messages[0].text)
        self.assertEqual("World", messages[1].text)


if __name__ == "__main__":
    unittest.main()
