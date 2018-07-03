# import unittest
#
# from doodledashboard.datafeeds.datafeed import Message
# from doodledashboard.filters.contains_text import ContainsTextFilter
# from doodledashboard.filters.matches_regex import MatchesRegexFilter
# from doodledashboard.updaters.image.image import ImageNotificationUpdater
#
#
# class TestImageHandler(unittest.TestCase):
#
#     def test_get_image_returns_none_when_no_image_filters(self):
#         handler = ImageNotificationUpdater({})
#         self.assertIsNone(handler.get_image())
#
#     def test_image_handler_update_works_when_no_image_filters(self):
#         handler = ImageNotificationUpdater({})
#         handler.update(Message(''))
#         self.assertIsNone(handler.get_image())
#
#     def test_get_image_returns_default_image_when_no_filters_set(self):
#         handler = ImageNotificationUpdater({})
#         handler.add_image_filter('/tmp/default.png')
#         self.assertEqual('/tmp/default.png', handler.get_image())
#
#     def test_get_image_returns_default_image_when_no_messages_match(self):
#         handler = ImageNotificationUpdater({})
#         handler.add_image_filter('/tmp/default.png')
#         handler.update(Message(''))
#
#         self.assertEqual('/tmp/default.png', handler.get_image())
#
#     def test_get_image_returns_correct_url_for_filtered_messages(self):
#         handler = ImageNotificationUpdater({})
#         handler.add_image_filter('/tmp/happy.png', ContainsTextFilter('123'))
#         handler.add_image_filter('/tmp/sad.png', MatchesRegexFilter('[4-6]+'))
#
#         handler.update(Message('123'))
#         self.assertEqual('/tmp/happy.png', handler.get_image())
#
#         handler.update(Message('456'))
#         self.assertEqual('/tmp/sad.png', handler.get_image())
#
#     def test_get_image_returns_previous_image_when_no_messages_match(self):
#         handler = ImageNotificationUpdater({})
#         handler.add_image_filter('/tmp/happy.png', ContainsTextFilter('123'))
#         handler.add_image_filter('/tmp/default.png')
#
#         handler.update(Message('123'))
#         self.assertEqual('/tmp/happy.png', handler.get_image())
#
#         handler.update(Message('Test'))
#         self.assertEqual('/tmp/happy.png', handler.get_image())
#
#
# if __name__ == '__main__':
#     unittest.main()
