import os
import unittest
import uuid

import pytest
from pytest_localserver import http

from doodledashboard.handlers.image.image import FileDownloader


@pytest.mark.usefixtures
class TestFileDownloader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()
        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    def test_file_correctly_downloaded_and_named(self):
        file_contents = str(uuid.uuid4())
        file_name = 'download-test.txt'

        self.http_server.serve_content(file_contents)

        image_downloader = FileDownloader()
        image_downloader.download('%s/%s' % (self.http_server.url, file_name))

        downloads = image_downloader.get_downloaded_files()
        self.assertEquals(1, len(downloads))

        file_path = downloads[0]
        self.assertTrue(file_name in file_path)

        with open(file_path, 'r') as f:
            self.assertEquals(file_contents, f.read())

        # Tidy up
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
