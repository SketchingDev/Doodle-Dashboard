import unittest

from mock import Mock

from doodledashboard.filters import MessageMatchesRegexFilter


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_regex_matches_single_message(self):
        message = TestMessageContainsTextFilter.create_mock_message_with_text('test1 test2')
        filtered_messages = MessageMatchesRegexFilter('test1|test3').filter([message])

        self.assertEqual(1, len(filtered_messages))

    def test_regex_matches_multiple_messages(self):
        message_1 = TestMessageContainsTextFilter.create_mock_message_with_text('test1')
        message_2 = TestMessageContainsTextFilter.create_mock_message_with_text('test2')

        filtered_messages = MessageMatchesRegexFilter('test1|test3').filter([message_1, message_2])

        self.assertEqual(1, len(filtered_messages))
        self.assertIn(message_1, filtered_messages)

    def test_regex_does_not_match(self):
        message = TestMessageContainsTextFilter.create_mock_message_with_text('test1 test2')
        filtered_messages = MessageMatchesRegexFilter('test3').filter([message])

        self.assertEqual(0, len(filtered_messages))

    @staticmethod
    def create_mock_message_with_text(text):
        message = Mock()
        message.get_text.return_value = text
        return message


if __name__ == '__main__':
    unittest.main()
