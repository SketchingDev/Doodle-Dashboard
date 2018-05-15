import unittest

from doodledashboard.datafeeds.datafeed import TextData
from doodledashboard.filters.message_contains_text import MessageContainsTextFilter
from doodledashboard.filters.message_matches_regex import MessageMatchesRegexFilter
from doodledashboard.handlers.image.image import ImageHandler


class TestImageHandler(unittest.TestCase):

    def test_get_image_returns_none_when_no_image_filters(self):
        handler = ImageHandler({})
        self.assertIsNone(handler.get_image())

    def test_image_handler_update_works_when_no_image_filters(self):
        handler = ImageHandler({})
        handler.update([TextData(''), TextData('')])
        self.assertIsNone(handler.get_image())

    def test_get_image_returns_default_image_when_no_filters_set(self):
        handler = ImageHandler({})
        handler.add_image_filter('/tmp/default.png')
        self.assertEqual('/tmp/default.png', handler.get_image())

    def test_get_image_returns_default_image_when_no_messages_match(self):
        handler = ImageHandler({})
        handler.add_image_filter('/tmp/default.png')
        handler.update([TextData('')])

        self.assertEqual('/tmp/default.png', handler.get_image())

    def test_get_image_returns_correct_url_for_filtered_messages(self):
        handler = ImageHandler({})
        handler.add_image_filter('/tmp/happy.png', MessageContainsTextFilter('123'))
        handler.add_image_filter('/tmp/sad.png', MessageMatchesRegexFilter('[4-6]+'))

        handler.update([TextData('123')])
        self.assertEqual('/tmp/happy.png', handler.get_image())

        handler.update([TextData('456'), TextData('789')])
        self.assertEqual('/tmp/sad.png', handler.get_image())

    def test_get_image_returns_previous_image_when_no_messages_match(self):
        handler = ImageHandler({})
        handler.add_image_filter('/tmp/happy.png', MessageContainsTextFilter('123'))
        handler.add_image_filter('/tmp/default.png')

        handler.update([TextData('123')])
        self.assertEqual('/tmp/happy.png', handler.get_image())

        handler.update([])
        self.assertEqual('/tmp/happy.png', handler.get_image())


if __name__ == '__main__':
    unittest.main()
