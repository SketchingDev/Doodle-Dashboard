import logging
import os
import tempfile
import urllib.request
from urllib.parse import urlparse


class FileDownloader:

    _FILENAME_CHAR_WHITELIST = "abcdefghijklmnopqrstuvwxyz0123456789-_"

    def __init__(self):
        self._downloaded_files = []
        self._logger = logging.getLogger(__name__)

    def download(self, url):
        filename_from_url = self._extract_filename(url)
        filename = "-doodledashboard-%s" % filename_from_url
        filename = filename.lower()
        filename = self._sanitise_filename(filename)

        fd, path = tempfile.mkstemp(filename)

        self._logger.info("Downloading %s to %s", url, path)
        with urllib.request.urlopen(url) as response, os.fdopen(fd, "wb") as out_file:
            out_file.write(response.read())

        self._downloaded_files.append(path)

        return path

    def get_downloaded_files(self):
        return self._downloaded_files

    def _sanitise_filename(self, unsafe_value):
        safe = ""
        for unsafe_char in unsafe_value:
            if unsafe_char in self._FILENAME_CHAR_WHITELIST:
                safe += unsafe_char
        return safe

    @staticmethod
    def _extract_filename(url):
        parsed_url = urlparse(url)
        return os.path.basename(parsed_url.path)
