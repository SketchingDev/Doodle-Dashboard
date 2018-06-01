import unittest

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import TextEntity
from doodledashboard.filters.contains_text import ContainsTextFilter, ContainsTextFilterSection


class TestMessageContainsTextFilter(unittest.TestCase):

    def test_filter_true_if_entity_contains_text(self):
        entity = TextEntity('1')
        self.assertTrue(ContainsTextFilter('1').filter(entity))

    def test_filter_false_if_entity_does_not_contain_text(self):
        entity = TextEntity('2')
        self.assertFalse(ContainsTextFilter('1').filter(entity))

    def test_filter_true_if_matching_text_empty(self):
        entity = TextEntity('1')
        self.assertTrue(ContainsTextFilter('').filter(entity))


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
