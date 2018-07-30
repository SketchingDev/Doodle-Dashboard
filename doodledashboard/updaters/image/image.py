import logging
import os
import tempfile
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlparse

from doodledashboard.configuration.config import MissingRequiredOptionException, HandlerCreationException, ConfigSection
from doodledashboard.filters.contains_text import ContainsTextFilter
from doodledashboard.filters.matches_regex import MatchesRegexFilter
from doodledashboard.updaters.updater import NotificationUpdater


class ImageNotificationUpdater(NotificationUpdater):
    """
    * First message that contains text that matches an image's filter
    """

    def __init__(self):
        super().__init__()
        self._filtered_images = []
        self._default_image_path = None
        self._chosen_image_path = None

    def add_image_filter(self, absolute_path, choice_filter=None):
        if choice_filter:
            self._filtered_images.append({"path": absolute_path, "filter": choice_filter})
        else:
            self._default_image_path = absolute_path

    def _update(self, notification, message):
        for image_filter in self._filtered_images:
            if image_filter["filter"].filter(message):
                self._chosen_image_path = image_filter["path"]

        if self._chosen_image_path:
            image_path = self._chosen_image_path
        else:
            image_path = self._default_image_path

        if image_path:
            notification.set_image_path(image_path)

    def get_filtered_images(self):
        return self._filtered_images

    @staticmethod
    def get_config_factory():
        return ImageNotificationUpdaterConfig()


class FileDownloader:

    _FILENAME_CHAR_WHITELIST = "abcdefghijklmnopqrstuvwxyz0123456789-_"

    def __init__(self):
        self._downloaded_files = []
        self._logger = logging.getLogger("doodledashboard")

    def download(self, url):
        filename_from_url = self._extract_filename(url)
        filename = "-doodledashboard-%s" % filename_from_url
        filename = filename.lower()
        filename = self._sanitise_filename(filename)

        fd, path = tempfile.mkstemp(filename)

        logging.info("Downloading %s to %s", [url, path])
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


class ImageNotificationUpdaterConfig(ConfigSection):

    def __init__(self, file_downloader=FileDownloader()):
        super().__init__()
        self._file_downloader = file_downloader

    @property
    def id_key_value(self):
        return "name", "image-depending-on-message-content"

    def create(self, config_section):
        updater = ImageNotificationUpdater()

        has_images = "images" in config_section
        has_default_image = "default-image" in config_section

        if not has_images and not has_default_image:
            raise MissingRequiredOptionException("Expected 'images' list and/or default-image to exist")

        if has_default_image:
            image_url = self._encode_url(config_section["default-image"])

            image_path = self.download(image_url)
            updater.add_image_filter(image_path)

        if has_images:
            for image_config_section in config_section["images"]:
                if "path" not in image_config_section:
                    raise MissingRequiredOptionException("Expected 'path' option to exist")

                image_url = self._encode_url(image_config_section["path"])

                image_filter = self._create_filter(image_config_section)
                image_path = self.download(image_url)

                updater.add_image_filter(image_path, image_filter)

        return updater

    def download(self, url):
        try:
            return self._file_downloader.download(url)
        except HTTPError as err:
            raise HandlerCreationException("Error '%s' when downloading %s" % (err.msg, err.url))

    @staticmethod
    def _encode_url(full_url):
        """
        Encode invalid characters in URL to provide, such as spaces.

        This implements code from the following URLs
        https://bugs.python.org/issue14826
        https://hg.python.org/cpython/rev/ebd37273e0fe
        """
        return urllib.parse.quote(full_url, safe="%/:=&?~#+!$,;'@()*[]|")

    @staticmethod
    def _create_filter(image_config_section):
        pattern_exists = "if-matches" in image_config_section
        contains_exists = "if-contains" in image_config_section

        if not pattern_exists and not contains_exists:
            raise MissingRequiredOptionException("Expected either 'if-contains' or 'if-matches' option to exist")

        if pattern_exists and contains_exists:
            raise MissingRequiredOptionException("Expected either 'if-contains' or 'if-matches' option, but not both")

        if pattern_exists:
            return MatchesRegexFilter(image_config_section["if-matches"])
        else:
            return ContainsTextFilter(image_config_section["if-contains"])
