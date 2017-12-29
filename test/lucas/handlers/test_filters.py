import unittest

from mock import Mock

from doodledashboard.lucas.handlers.filters import MessageContainsTextFilter


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_message_returned_that_contain_text_passed_to_constructor(self):
        message_1 = TestMessageContainsTextFilter.create_mock_message_with_text('1')
        message_2 = TestMessageContainsTextFilter.create_mock_message_with_text('2')

        messages = MessageContainsTextFilter('1').filter([message_1, message_2])

        self.assertEqual(messages, [message_1])

    def test_all_messages_returned_if_blank_text_passed_in(self):
        message_1 = TestMessageContainsTextFilter.create_mock_message_with_text('1')
        message_2 = TestMessageContainsTextFilter.create_mock_message_with_text('2')

        messages = MessageContainsTextFilter('').filter([message_1, message_2])

        self.assertEqual(messages, [message_1, message_2])

    def test_no_messages_returned_when_no_messages_passed_in(self):
        messages = MessageContainsTextFilter('').filter([])
        self.assertEqual(messages, [])

    def test_text_returned_by_remove_text_does_not_contain_text_passed_into_constructor(self):
        message = TestMessageContainsTextFilter.create_mock_message_with_text('123')

        text = MessageContainsTextFilter('2').remove_text(message)
        self.assertEqual(text, '13')

    @staticmethod
    def create_mock_message_with_text(text):
        message = Mock()
        message.get_text.return_value = text
        return message


if __name__ == '__main__':
    unittest.main()
