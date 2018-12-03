import os
import pytest
import unittest
import uuid
from pytest_localserver import http

from doodledashboard.notifications.image.file_downloader import FileDownloader


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

    def test_local_filename_created_from_remote_filename_is_safe(self):
        """
        Inelegant parameterised test created because pytest doesn't appear to allow
        parameterised tests with fixtures.
        """

        remote_with_expected_local = [
            ["hello-world.txt", "hello-worldtxt", "dot in filename"],
            ["", "-", "no filename"],
            ["..", "-", "escape directory"],
            ["//", "-", "sub-directory"],
            ["hello%20world", "hello20world", "filename with a space"]
        ]

        for item in remote_with_expected_local:
            remote_filename = item[0]
            expected_end_of_local_filename = item[1]
            description = item[2]

            self.downloaded_file_has_correct_name(
                remote_filename,
                expected_end_of_local_filename,
                description
            )

    def downloaded_file_has_correct_name(self, remote_name, expected_end_of_local_filename, description):
        file_contents = str(uuid.uuid4())

        self.http_server.serve_content(file_contents)
        url = '%s/%s' % (self.http_server.url, remote_name)

        image_downloader = FileDownloader()
        image_downloader.download(url)

        downloads = image_downloader.get_downloaded_files()
        self.assertEqual(1, len(downloads), "File has been downloaded")

        file_path = downloads[0]
        self.assertTrue(
            file_path.endswith(expected_end_of_local_filename),
            "Expected local path '%s' to end with '%s'" % (file_path, expected_end_of_local_filename))

        with open(file_path, 'r') as f:
            self.assertEquals(file_contents, f.read())

        # Tidy up
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
