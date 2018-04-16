from doodledashboard.config import MissingRequiredOptionException
from doodledashboard.filters import MessageMatchesRegexFilter, MessageContainsTextFilter
from doodledashboard.handlers.handler import MessageHandler, MessageHandlerConfigCreator
import urllib2
import tempfile
import urlparse
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
                return

        self._chosen_image_path = self._default_image_path

    def draw(self, display):
        display.draw_image(self._chosen_image_path, 0, 0, display.get_size())
        display.flush()

    def get_filtered_images(self):
        return self._filtered_images

    def get_image(self):
        if self._chosen_image_path:
            return self._chosen_image_path
        else:
            return self._default_image_path

    def __str__(self):
        return 'Image handler with %s images' % len(self._filtered_images)


class FileDownloader:

    def __init__(self):
        self._downloaded_files = []

    def download(self, url):
        data = urllib2.urlopen(url)

        fd, path = tempfile.mkstemp("-%s" % self._extract_filename(url))
        with os.fdopen(fd, 'w') as f:
            f.write(data.read())

        self._downloaded_files.append(path)

        return path

    def get_downloaded_files(self):
        return self._downloaded_files

    @staticmethod
    def _extract_filename(url):
        parsed_url = urlparse.urlparse(url)
        return os.path.basename(parsed_url.path)


class ImageMessageHandlerConfigCreator(MessageHandlerConfigCreator):
    def __init__(self, key_value_storage, file_downloader):
        MessageHandlerConfigCreator.__init__(self, key_value_storage)
        self._file_downloader = file_downloader

    def creates_for_id(self, filter_id):
        return filter_id == 'image-handler'

    def create_handler(self, config_section, key_value_store):
        if 'images' not in config_section:
            raise MissingRequiredOptionException("Expected 'images' list to exist")

        handler = ImageHandler(key_value_store)

        if 'default-image' in config_section:
            handler.add_image_filter(config_section['default-image'])

        for image_config_section in config_section['images']:
            if 'uri' not in image_config_section:
                raise MissingRequiredOptionException("Expected 'uri' option to exist")

            image_uri = image_config_section["uri"]
            image_filter = self._create_filter(image_config_section)

            image_path = self._file_downloader.download(image_uri)
            handler.add_image_filter(image_path, image_filter)

        return handler

    @staticmethod
    def _create_filter(image_config_section):
        pattern_exists = 'pattern' in image_config_section
        contains_exists = 'contains' in image_config_section

        if not pattern_exists and not contains_exists:
            raise MissingRequiredOptionException("Expected either 'pattern' or 'contains' option to exist")

        if pattern_exists and contains_exists:
            raise MissingRequiredOptionException("Expected either 'pattern' or 'contains' option, but not both")

        if pattern_exists:
            return MessageMatchesRegexFilter(image_config_section['pattern'])
        else:
            return MessageContainsTextFilter(image_config_section['contains'])
