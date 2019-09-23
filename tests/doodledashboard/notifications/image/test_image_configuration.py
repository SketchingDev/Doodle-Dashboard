import os
import unittest
import uuid

import pytest
from pytest_localserver import http

from doodledashboard.component import MissingRequiredOptionException
from doodledashboard.datafeeds.datafeed import Message
from doodledashboard.filters.contains_text import ContainsTextFilter
from doodledashboard.filters.matches_regex import MatchesRegexFilter
from doodledashboard.notifications.image.file_downloader import FileDownloader
from doodledashboard.notifications.image.image import ImageDependingOnMessageContent, \
    ImageDependingOnMessageContentCreator


@pytest.mark.usefixtures
class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}
    _EMPTY_SECRET_STORE = {}

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_id_is_image_depending_on_message_content(self):
        id = ImageDependingOnMessageContentCreator.get_id()
        self.assertEqual("image-depending-on-message-content", id)

    def test_exception_raised_when_no_image_list_and_default_image_in_options(self):
        config = ImageDependingOnMessageContentCreator()

        with pytest.raises(MissingRequiredOptionException) as exception:
            config.create(self._EMPTY_OPTIONS, self._EMPTY_SECRET_STORE)
        self.assertEqual("Expected 'images' list and/or default-image to exist", exception.value.message)

    def test_exception_raised_when_image_missing_path_in_options(self):
        config = ImageDependingOnMessageContentCreator()
        options = {
            "images": [
                {}
            ]
        }

        with pytest.raises(MissingRequiredOptionException) as exception:
            config.create(options, {})

        self.assertEqual("Expected 'path' option to exist", exception.value.message)

    def test_exception_raised_when_image_in_list_missing_pattern_and_contains(self):
        config = ImageDependingOnMessageContentCreator()
        options = {
            "images": [
                {"path": "test"}
            ]
        }

        with pytest.raises(MissingRequiredOptionException) as exception:
            config.create(options, {})

        self.assertEqual("Expected either 'if-contains' or 'if-matches' option to exist", exception.value.message)

    def test_exception_raised_when_image_in_list_image_contains_pattern_and_contains(self):
        options = {
            "images": [
                {
                    "path": "test",
                    "if-matches": "test",
                    "if-contains": "test"
                }
            ]
        }

        config = ImageDependingOnMessageContentCreator()

        with pytest.raises(MissingRequiredOptionException) as exception:
            config.create(options, {})

        self.assertEqual("Expected either 'if-contains' or 'if-matches' option, but not both", exception.value.message)

    def test_output_created_with_path_and_pattern(self):
        self.http_server.serve_content("<IMAGE CONTENT>")

        downloader = FileDownloader()
        config = ImageDependingOnMessageContentCreator(downloader)
        options = {
            "images": [
                {
                    "path": "%s/test-filename-1.png" % self.http_server.url,
                    "if-matches": "test pattern1"
                }
            ]
        }

        try:
            config = config.create(options, self._EMPTY_SECRET_STORE)
            self.assertIsInstance(config, ImageDependingOnMessageContent)

            image_filters = config.filtered_images
            self.assertEqual(1, len(image_filters), "Single image has been configured")

            image_and_filter = image_filters[0]

            downloaded_files = downloader.get_downloaded_files()
            self.assertEqual(1, len(downloaded_files), "Single image has been downloaded")
            download_path = downloaded_files[0]

            self.assertEqual(download_path, image_and_filter["path"],
                             "Image path in handler matches path to downloaded file")
            self.assertEqual("test pattern1", str(image_and_filter["filter"].pattern),
                             "Image filter's pattern matches configuration")
        finally:
            self.cleanup_downloaded_files(downloader, "test-filename-1.png")

    def test_output_created_with_path_and_contains(self):
        self.http_server.serve_content('<IMAGE CONTENT>')

        downloader = FileDownloader()
        config = ImageDependingOnMessageContentCreator(downloader)
        options = {
            "images": [
                {
                    "path": "%s/test-filename-2.png" % self.http_server.url,
                    "if-contains": "test pattern2"
                }
            ]
        }

        try:
            notification = config.create(options, self._EMPTY_SECRET_STORE)
            image_filters = notification.filtered_images

            self.assertEqual(1, len(image_filters), "Single image has been configured")
            image_and_filter = image_filters[0]

            downloaded_files = downloader.get_downloaded_files()
            self.assertEqual(1, len(downloaded_files), "Single image has been downloaded")
            download_path = downloaded_files[0]

            self.assertEqual(download_path, image_and_filter["path"],
                             "Image path in handler matches path to downloaded file")
            self.assertEqual("test pattern2", str(image_and_filter["filter"].text),
                             "Image filter's 'contains' matches configuration")
        finally:
            self.cleanup_downloaded_files(downloader, "test-filename-2.png")

    def test_output_created_with_default_image(self):
        self.http_server.serve_content("<IMAGE CONTENT>")

        downloader = FileDownloader()
        config = ImageDependingOnMessageContentCreator(downloader)
        options = {
            "default-image": "%s/default-image.png" % self.http_server.url
        }

        try:
            notification = config.create(options, self._EMPTY_SECRET_STORE)

            downloaded_files = downloader.get_downloaded_files()
            self.assertEqual(1, len(downloaded_files))
            download_path = downloaded_files[0]

            self.assertEqual(
                download_path,
                notification.default_image,
                "Image path in handler matches path to downloaded file"
            )
        finally:
            self.cleanup_downloaded_files(downloader, "default-image.png")

    def test_notification_encodes_image_path_in_output(self):
        file_contents = str(uuid.uuid4())

        self.http_server.serve_content(file_contents)

        downloader = FileDownloader()
        config = ImageDependingOnMessageContentCreator(downloader)
        options = {
            "default-image": "%s/default image.png" % self.http_server.url
        }

        try:
            notification = config.create(options, self._EMPTY_SECRET_STORE)
            image_output = notification.create([])

            self.assertIsNotNone(image_output.image_path)
            with open(image_output.image_path, 'r') as f:
                self.assertEquals(file_contents, f.read())

        finally:
            self.cleanup_downloaded_files(downloader, "default20image.png")

    @staticmethod
    def cleanup_downloaded_files(downloader, filename):
        for downloaded_file in downloader.get_downloaded_files():
            if downloaded_file.endswith(filename):
                os.remove(downloaded_file)

    class TestNotification(unittest.TestCase):

        def test_no_image_output_produced_when_no_messages(self):
            notification = ImageDependingOnMessageContent()
            image_output = notification.create([])

            self.assertIsNone(image_output)

        def test_no_image_output_produced_when_no_images_specified(self):
            notification = ImageDependingOnMessageContent()
            image_output = notification.create([Message("Test 123")])

            self.assertIsNone(image_output)

        def test_image_output_produced_contains_default_image_when_no_other_images_set(self):
            notification = ImageDependingOnMessageContent()
            notification.add_image_filter("/tmp/default.png")

            image_output = notification.create([])

            self.assertEqual("/tmp/default.png", image_output.image_path)

        def test_image_output_produced_contains_url_for_filter_that_matches_the_last_message(self):
            notification = ImageDependingOnMessageContent()
            notification.add_image_filter("/tmp/happy.png", ContainsTextFilter("123"))
            notification.add_image_filter("/tmp/sad.png", MatchesRegexFilter("[4-6]+"))

            image_output = notification.create([Message("123")])
            self.assertEqual('/tmp/happy.png', image_output.image_path)

            image_output = notification.create([Message("456")])
            self.assertEqual('/tmp/sad.png', image_output.image_path)

        def test_image_output_produced_contains_url_for_last_match_if_no_current_images_match(self):
            notification = ImageDependingOnMessageContent()
            notification.add_image_filter("/tmp/happy.png", ContainsTextFilter("123"))
            notification.add_image_filter("/tmp/default.png")

            image_output = notification.create([Message("123")])
            self.assertEqual('/tmp/happy.png', image_output.image_path)

            image_output = notification.create([Message("Test")])
            self.assertEqual('/tmp/happy.png', image_output.image_path)


if __name__ == "__main__":
    unittest.main()
