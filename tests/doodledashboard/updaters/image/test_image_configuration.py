import os
import pytest
import unittest
import uuid
from pytest_localserver import http

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.notifications import ImageNotification
from doodledashboard.updaters.image.image import FileDownloader, ImageNotificationUpdater, \
    ImageNotificationUpdaterConfig


@pytest.mark.usefixtures
class TestImageNotificationUpdaterConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_can_create_returns_false_for_empty_config(self):
        config = {}

        creator = ImageNotificationUpdaterConfig(None)
        self.assertFalse(creator.can_create(config))

    def test_can_create_returns_false_for_incorrect_handler(self):
        config = {
            "name": "wrong-id"
        }

        creator = ImageNotificationUpdaterConfig(None)
        self.assertFalse(creator.can_create(config))

    def test_exception_thrown_if_config_missing_images_list_and_default_image(self):
        config = {
            "name": "image-depending-on-message-content"
        }

        creator = ImageNotificationUpdaterConfig(None)
        self.assertTrue(creator.can_create(config))

        with pytest.raises(MissingRequiredOptionException) as exception:
            creator.create(config)
        self.assertEqual("Expected 'images' list and/or default-image to exist", exception.value.value)

    def test_exception_thrown_if_config_images_list_missing_image_path(self):
        config = {
            "name": "image-depending-on-message-content",
            "images": [
                {}
            ]
        }

        creator = ImageNotificationUpdaterConfig(None)
        self.assertTrue(creator.can_create(config))

        with pytest.raises(MissingRequiredOptionException) as exception:
            creator.create(config)
        self.assertEqual("Expected 'path' option to exist", exception.value.value)

    def test_exception_thrown_if_config_images_list_missing_image_pattern_and_contains(self):
        config = {
            "name": "image-depending-on-message-content",
            "images": [
                {"path": "test"}
            ]
        }

        creator = ImageNotificationUpdaterConfig(None)
        self.assertTrue(creator.can_create(config))

        with pytest.raises(MissingRequiredOptionException) as exception:
            creator.create(config)
        self.assertEqual("Expected either 'if-contains' or 'if-matches' option to exist", exception.value.value)

    def test_exception_thrown_if_config_images_list_image_contains_pattern_and_contains(self):
        config = {
            "name": "image-depending-on-message-content",
            "images": [
                {
                    "path": "test",
                    "if-matches": "test",
                    "if-contains": "test"
                }
            ]
        }

        creator = ImageNotificationUpdaterConfig(None)
        self.assertTrue(creator.can_create(config))

        with pytest.raises(MissingRequiredOptionException) as exception:
            creator.create(config)
        self.assertEqual(
            "Expected either 'if-contains' or 'if-matches' option, but not both",
            exception.value.value
        )

    def test_handler_created_with_path_and_pattern(self):
        self.http_server.serve_content("<IMAGE CONTENT>")

        config = {
            "name": "image-depending-on-message-content",
            "images": [
                {
                    "path": "%s/test-filename-1.png" % self.http_server.url,
                    "if-matches": "test pattern1"
                }
            ]
        }

        downloader = FileDownloader()
        creator = ImageNotificationUpdaterConfig(downloader)
        self.assertTrue(creator.can_create(config))

        try:
            updater = creator.create(config)
            self.assertIsInstance(updater, ImageNotificationUpdater)

            image_filters = updater.get_filtered_images()
            self.assertEqual(1, len(image_filters))

            image_and_filter = image_filters[0]

            downloaded_files = downloader.get_downloaded_files()
            self.assertEqual(1, len(downloaded_files))
            download_path = downloaded_files[0]

            self.assertEqual(download_path, image_and_filter["path"],
                             "Image path in handler matches path to downloaded file")
            self.assertEqual("test pattern1", str(image_and_filter["filter"].get_pattern()),
                             "Image filter's pattern matches configuration")
        finally:
            self.cleanup_downloaded_files(downloader, "test-filename-1.png")

    def test_handler_created_with_path_and_contains(self):
        self.http_server.serve_content('<IMAGE CONTENT>')

        config = {
            "name": "image-depending-on-message-content",
            "images": [
                {
                    "path": "%s/test-filename-2.png" % self.http_server.url,
                    "if-contains": "test pattern2"
                }
            ]
        }

        downloader = FileDownloader()
        creator = ImageNotificationUpdaterConfig(downloader)
        self.assertTrue(creator.can_create(config))

        try:
            handler = creator.create(config)
            image_filters = handler.get_filtered_images()

            self.assertEqual(1, len(image_filters))
            image_and_filter = image_filters[0]

            downloaded_files = downloader.get_downloaded_files()
            self.assertEqual(1, len(downloaded_files))
            download_path = downloaded_files[0]

            self.assertEqual(download_path, image_and_filter["path"],
                             "Image path in handler matches path to downloaded file")
            self.assertEqual("test pattern2", str(image_and_filter["filter"].get_text()),
                             "Image filter's 'contains' matches configuration")
        finally:
            self.cleanup_downloaded_files(downloader, "test-filename-2.png")

    def test_handler_created_with_default_image(self):
        self.http_server.serve_content("<IMAGE CONTENT>")

        config = {
            "name": "image-depending-on-message-content",
            "default-image": "%s/default-image.png" % self.http_server.url
        }

        downloader = FileDownloader()
        creator = ImageNotificationUpdaterConfig(downloader)
        self.assertTrue(creator.can_create(config))

        try:
            updater = creator.create(config)
            notification = ImageNotification()
            updater.update(notification, None)

            downloaded_files = downloader.get_downloaded_files()
            self.assertEqual(1, len(downloaded_files))
            download_path = downloaded_files[0]

            self.assertEqual(
                download_path,
                notification.get_image_path(),
                "Image path in handler matches path to downloaded file"
            )
        finally:
            self.cleanup_downloaded_files(downloader, "default-image.png")

    def test_handler_created_with_default_image_path_encoded(self):
        file_contents = str(uuid.uuid4())

        self.http_server.serve_content(file_contents)

        config = {
            "name": "image-depending-on-message-content",
            "default-image": "%s/default image.png" % self.http_server.url
        }

        downloader = FileDownloader()
        creator = ImageNotificationUpdaterConfig(downloader)

        try:
            updater = creator.create(config)
            notification = ImageNotification()
            updater.update(notification, None)

            self.assertIsNotNone(notification.get_image_path())
            with open(notification.get_image_path(), 'r') as f:
                self.assertEquals(file_contents, f.read())

        finally:
            self.cleanup_downloaded_files(downloader, "default20image.png")

    @staticmethod
    def cleanup_downloaded_files(downloader, filename):
        for downloaded_file in downloader.get_downloaded_files():
            if downloaded_file.endswith(filename):
                os.remove(downloaded_file)


if __name__ == "__main__":
    unittest.main()
