import unittest

from doodledashboard.component import DataFeedConfig
from doodledashboard.configuration import ComponentConfigParser
from doodledashboard.datafeeds.datafeed import DataFeed


class DummyFeed(DataFeed):

    def __init__(self, options):
        super().__init__()
        self.options = options

    def get_latest_messages(self):
        return []


class DummyFeedConfig(DataFeedConfig):

    @staticmethod
    def get_id():
        return "test-feed"

    def create(self, options, secret_store):
        return DummyFeed(options)


class TestComponentConfigParser(unittest.TestCase):
    _EMPTY_SECRET_STORE = {}

    def test_name_is_set_against_component(self):
        abc = ComponentConfigParser([DummyFeedConfig()], self._EMPTY_SECRET_STORE)
        component = abc.parse({
            'name': 'test-name',
            'type': 'test-feed',
            'options': {
                'option-1': 'test-value-1'
            }
        })

        self.assertEqual(component.name, 'test-name')
        self.assertEqual(component.options, {
            'option-1': 'test-value-1'
        })

    def test_options_are_passed_to_create_method_of_config(self):
        abc = ComponentConfigParser([DummyFeedConfig()], self._EMPTY_SECRET_STORE)
        component = abc.parse({
            'type': 'test-feed',
            'options': {
                'option-1': 'test-value-1'
            }
        })

        self.assertEqual(component.options, {
            'option-1': 'test-value-1'
        })


if __name__ == '__main__':
    unittest.main()
