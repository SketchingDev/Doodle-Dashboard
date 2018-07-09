import unittest

from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.contains_text import ContainsTextFilter
from doodledashboard.filters.matches_regex import MatchesRegexFilter
from doodledashboard.notifications import ImageNotification
from doodledashboard.updaters.image.image import ImageNotificationUpdater


class TestImageHandler(unittest.TestCase):

    def test_get_image_returns_none_when_no_image_filters(self):
        notification = ImageNotification()

        updater = ImageNotificationUpdater()
        updater.update(notification, None)

        self.assertIsNone(notification.get_image_path())

    def test_image_handler_update_works_when_no_image_filters(self):
        notification = ImageNotification()

        updater = ImageNotificationUpdater()
        updater.update(notification, None)

        self.assertIsNone(notification.get_image_path())

    def test_get_image_returns_default_image_when_no_filters_set(self):
        notification = ImageNotification()

        updater = ImageNotificationUpdater()
        updater.add_image_filter("/tmp/default.png")
        updater.update(notification, None)

        self.assertEqual("/tmp/default.png", notification.get_image_path())

    def test_get_image_returns_default_image_when_no_messages_match(self):
        notification = ImageNotification()

        updater = ImageNotificationUpdater()
        updater.add_image_filter("/tmp/default.png")
        updater.update(notification, None)

        self.assertEqual('/tmp/default.png', notification.get_image_path())

    def test_get_image_returns_correct_url_for_filtered_messages(self):
        notification = ImageNotification()

        updater = ImageNotificationUpdater()
        updater.add_image_filter("/tmp/happy.png", ContainsTextFilter("123"))
        updater.add_image_filter("/tmp/sad.png", MatchesRegexFilter("[4-6]+"))

        updater.update(notification, Message("123"))
        self.assertEqual('/tmp/happy.png', notification.get_image_path())

        updater.update(notification, Message("456"))
        self.assertEqual('/tmp/sad.png', notification.get_image_path())

    def test_get_image_returns_previous_image_when_no_messages_match(self):
        notification = ImageNotification()

        updater = ImageNotificationUpdater()
        updater.add_image_filter("/tmp/happy.png", ContainsTextFilter("123"))
        updater.add_image_filter("/tmp/default.png")

        updater.update(notification, Message("123"))
        self.assertEqual('/tmp/happy.png', notification.get_image_path())

        updater.update(notification, Message("Test"))
        self.assertEqual('/tmp/happy.png', notification.get_image_path())


if __name__ == '__main__':
    unittest.main()
