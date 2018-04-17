import unittest

from mock import Mock

from doodledashboard.config import MissingRequiredOptionException
from doodledashboard.filters import MessageContainsTextFilter, MessageContainsTextFilterCreator


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_message_returned_that_contain_text_passed_to_constructor(self):
        message_1 = TestMessageContainsTextFilter.create_mock_message_with_text('1')
        message_2 = TestMessageContainsTextFilter.create_mock_message_with_text('2')

        messages = MessageContainsTextFilter('1').filter([message_1, message_2])

        self.assertEqual([message_1], messages)

    def test_all_messages_returned_if_blank_text_passed_in(self):
        message_1 = TestMessageContainsTextFilter.create_mock_message_with_text('1')
        message_2 = TestMessageContainsTextFilter.create_mock_message_with_text('2')

        messages = MessageContainsTextFilter('').filter([message_1, message_2])

        self.assertEqual([message_1, message_2], messages)

    def test_no_messages_returned_when_no_messages_passed_in(self):
        messages = MessageContainsTextFilter('').filter([])
        self.assertEqual([], messages)

    def test_text_returned_by_remove_text_does_not_contain_text_passed_into_constructor(self):
        message = TestMessageContainsTextFilter.create_mock_message_with_text('123')

        text = MessageContainsTextFilter('2').remove_text(message)
        self.assertEqual('13', text)

    @staticmethod
    def create_mock_message_with_text(text):
        message = Mock()
        message.get_text.return_value = text
        return message


class TestMessageContainsTextFilterCreator(unittest.TestCase):

    def test_creates_for_correct_id(self):
        self.assertTrue(MessageContainsTextFilterCreator().creates_for_id('message-contains-text'))

    def test_exception_thrown_for_missing_text_option(self):
        creator = MessageContainsTextFilterCreator()

        with self.assertRaises(MissingRequiredOptionException):
            creator.create({'type': 'message-contains-text'})

    def test_text_options_passed_to_filter(self):
        creator = MessageContainsTextFilterCreator()

        text_filter = creator.create({
            'type': 'message-contains-text',
            'text': 'testing'
        })

        self.assertEqual('testing', text_filter.get_text())


if __name__ == '__main__':
    unittest.main()
