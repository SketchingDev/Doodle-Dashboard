import unittest

from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.matches_regex import MatchesRegexFilter


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_regex_matches_single_message(self):
        message = Message('test1 test2')
        filtered_message = MatchesRegexFilter('test1|test3').filter(message)

        self.assertTrue(filtered_message)

    def test_regex_matches_multiple_messages(self):
        message = Message('test 2')

        filtered_message = MatchesRegexFilter('test1|test3').filter(message)

        self.assertFalse(filtered_message)

    def test_regex_does_not_match(self):
        message = Message('test1 test2')
        filtered_message = MatchesRegexFilter('test3').filter(message)

        self.assertFalse(filtered_message)


if __name__ == '__main__':
    unittest.main()
