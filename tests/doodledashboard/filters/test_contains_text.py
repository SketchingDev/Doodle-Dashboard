import unittest

from mock import Mock

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.filters.contains_text import ContainsTextFilter, ContainsTextFilterSection


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_message_returned_that_contain_text_passed_to_constructor(self):
        message_1 = TestMessageContainsTextFilter.create_mock_text_entity('1')
        message_2 = TestMessageContainsTextFilter.create_mock_text_entity('2')

        messages = ContainsTextFilter('1').filter([message_1, message_2])

        self.assertEqual([message_1], messages)

    def test_all_messages_returned_if_blank_text_passed_in(self):
        entity_1 = TestMessageContainsTextFilter.create_mock_text_entity('1')
        entity_2 = TestMessageContainsTextFilter.create_mock_text_entity('2')

        entities = ContainsTextFilter('').filter([entity_1, entity_2])

        self.assertEqual([entity_1, entity_2], entities)

    def test_no_messages_returned_when_no_messages_passed_in(self):
        entities = ContainsTextFilter('').filter([])
        self.assertEqual([], entities)

    def test_text_returned_by_remove_text_does_not_contain_text_passed_into_constructor(self):
        entity = TestMessageContainsTextFilter.create_mock_text_entity('123')

        text = ContainsTextFilter('2').remove_text(entity)
        self.assertEqual('13', text)

    @staticmethod
    def create_mock_text_entity(text):
        entity = Mock()
        entity.get_text.return_value = text
        return entity


class TestContainsTextFilterCreator(unittest.TestCase):

    def test_creates_for_correct_id(self):
        self.assertTrue(ContainsTextFilterSection().creates_for_id('message-contains-text'))

    def test_exception_thrown_for_missing_text_option(self):
        creator = ContainsTextFilterSection()

        with self.assertRaises(MissingRequiredOptionException):
            creator.create({'type': 'message-contains-text'})

    def test_text_options_passed_to_filter(self):
        creator = ContainsTextFilterSection()

        text_filter = creator.create({
            'type': 'message-contains-text',
            'text': 'testing'
        })

        self.assertEqual('testing', text_filter.get_text())


if __name__ == '__main__':
    unittest.main()
