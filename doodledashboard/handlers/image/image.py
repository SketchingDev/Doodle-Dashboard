import logging

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.filters.contains_text import ContainsTextFilter
from doodledashboard.filters.matches_regex import MatchesRegexFilter
from doodledashboard.handlers.handler import MessageHandler, MessageHandlerConfigSection
import urllib.request
import tempfile
from urllib.parse import urlparse
import os


class ImageHandler(MessageHandler):
    """
    * First message that contains text that matches an image's filter
    """

    def __init__(self, key_value_store):
        MessageHandler.__init__(self, key_value_store)
        self._filtered_images = []
        self._default_image_path = None
        self._chosen_image_path = None

    def add_image_filter(self, absolute_path, choice_filter=None):
        if choice_filter:
            self._filtered_images.append({"path": absolute_path, "filter": choice_filter})
        else:
            self._default_image_path = absolute_path

    def update(self, messages):
        for image_filter in self._filtered_images:
            if image_filter["filter"].do_filter(messages):
                self._chosen_image_path = image_filter["path"]

    def draw(self, display):
        if self._chosen_image_path:
            image = self._chosen_image_path
        else:
            image = self._default_image_path

        if image:
            display.draw_image(image)

    def get_filtered_images(self):
        return self._filtered_images

    def get_image(self):
        if self._chosen_image_path:
            return self._chosen_image_path
        else:
            return self._default_image_path

    def __str__(self):
        return "Image handler with %s images" % len(self._filtered_images)


class FileDownloader:

    def __init__(self):
        self._downloaded_files = []
        self._logger = logging.getLogger("doodledashboard")

    def download(self, url):
        fd, path = tempfile.mkstemp("-doodledashboard-%s" % self._extract_filename(url))

        logging.info("Downloading %s to %s", [url, path])
        with urllib.request.urlopen(url) as response, os.fdopen(fd, "wb") as out_file:
            out_file.write(response.read())

        self._downloaded_files.append(path)

        return path

    def get_downloaded_files(self):
        return self._downloaded_files

    @staticmethod
    def _extract_filename(url):
        parsed_url = urlparse(url)
        return os.path.basename(parsed_url.path)


class ImageMessageHandlerConfigCreator(MessageHandlerConfigSection):
    def __init__(self, key_value_storage, file_downloader):
        MessageHandlerConfigSection.__init__(self, key_value_storage)
        self._file_downloader = file_downloader

    def creates_for_id(self, filter_id):
        return filter_id == "image-handler"

    def create_handler(self, config_section, key_value_store):
        handler = ImageHandler(key_value_store)

        has_images = "images" in config_section
        has_default_image = "default-image" in config_section

        if not has_images and not has_default_image:
            raise MissingRequiredOptionException("Expected 'images' list and/or default-image to exist")

        if has_default_image:
            image_path = self._file_downloader.download(config_section["default-image"])
            handler.add_image_filter(image_path)

        if has_images:
            for image_config_section in config_section["images"]:
                if "uri" not in image_config_section:
                    raise MissingRequiredOptionException("Expected 'uri' option to exist")

                image_uri = image_config_section["uri"]
                image_filter = self._create_filter(image_config_section)

                image_path = self._file_downloader.download(image_uri)
                handler.add_image_filter(image_path, image_filter)

        return handler

    @staticmethod
    def _create_filter(image_config_section):
        pattern_exists = "pattern" in image_config_section
        contains_exists = "contains" in image_config_section

        if not pattern_exists and not contains_exists:
            raise MissingRequiredOptionException("Expected either 'pattern' or 'contains' option to exist")

        if pattern_exists and contains_exists:
            raise MissingRequiredOptionException("Expected either 'pattern' or 'contains' option, but not both")

        if pattern_exists:
            return MatchesRegexFilter(image_config_section["pattern"])
        else:
            return ContainsTextFilter(image_config_section["contains"])
