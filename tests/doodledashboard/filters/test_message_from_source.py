import unittest

import pytest

from doodledashboard.component import MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.message_from_source import MessageFromSourceFilterConfig, MessageFromSourceFilter


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}

    def test_id_is_message_from_source(self):
        self.assertEqual("message-from-source", MessageFromSourceFilterConfig().get_id())

    def test_exception_raised_when_no_source_name_in_options(self):
        with pytest.raises(MissingRequiredOptionException) as err_info:
            MessageFromSourceFilterConfig().create(self._EMPTY_OPTIONS)

        self.assertEqual("Expected 'source-name' option to exist", err_info.value.message)

    def test_filter_from_config_factory_configured_correctly(self):
        source_filter = MessageFromSourceFilterConfig().create({'source-name': 'test-config-source-name'})
        self.assertEqual(source_filter.source_name, 'test-config-source-name')


class TestFilter(unittest.TestCase):

    def test_filter_true_if_message_source_matches_filter(self):
        message = Message('', 'test-source')
        self.assertTrue(MessageFromSourceFilter('test-source').filter(message))

    def test_filter_false_if_message_source_does_not_match_filter(self):
        message = Message('', 'test-source-2')
        self.assertFalse(MessageFromSourceFilter('test-source').filter(message))

    def test_filter_true_if_matching_source_empty(self):
        message = Message('')
        self.assertTrue(MessageFromSourceFilter('').filter(message))


if __name__ == '__main__':
    unittest.main()
