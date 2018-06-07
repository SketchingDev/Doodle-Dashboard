import unittest

from doodledashboard.datafeeds.datafeed import TextEntity
from doodledashboard.filters.matches_regex import MatchesRegexFilter


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_regex_matches_single_message(self):
        message = TextEntity('test1 test2')
        filtered_message = MatchesRegexFilter('test1|test3').filter(message)

        self.assertTrue(filtered_message)

    def test_regex_matches_multiple_messages(self):
        message = TextEntity('test 2')

        filtered_message = MatchesRegexFilter('test1|test3').filter(message)

        self.assertFalse(filtered_message)

    def test_regex_does_not_match(self):
        message = TextEntity('test1 test2')
        filtered_message = MatchesRegexFilter('test3').filter(message)

        self.assertFalse(filtered_message)


if __name__ == '__main__':
    unittest.main()
