import unittest

import pytest

from doodledashboard.component import MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.contains_text import ContainsTextFilter, ContainsTextFilterCreator


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}
    _EMPTY_SECRET_STORE = {}

    def test_id_is_message_contains_text(self):
        self.assertEqual("message-contains-text", ContainsTextFilterCreator().get_id())

    def test_exception_raised_when_no_text_in_options(self):
        with pytest.raises(MissingRequiredOptionException) as err_info:
            ContainsTextFilterCreator().create(self._EMPTY_OPTIONS, self._EMPTY_SECRET_STORE)

        self.assertEqual("Expected 'text' option to exist", err_info.value.message)


class TestFilter(unittest.TestCase):

    def test_filter_true_if_entity_contains_text(self):
        entity = Message('1')
        self.assertTrue(ContainsTextFilter('1').filter(entity))

    def test_filter_false_if_entity_does_not_contain_text(self):
        entity = Message('2')
        self.assertFalse(ContainsTextFilter('1').filter(entity))

    def test_filter_true_if_matching_text_empty(self):
        entity = Message('1')
        self.assertTrue(ContainsTextFilter('').filter(entity))


if __name__ == '__main__':
    unittest.main()
