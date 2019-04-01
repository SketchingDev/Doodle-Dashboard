import urllib.request
from urllib.error import HTTPError
import urllib.parse

from doodledashboard.component import ComponentConfig, MissingRequiredOptionException, NotificationConfig, \
    ComponentCreationException
from doodledashboard.filters.contains_text import ContainsTextFilter
from doodledashboard.filters.matches_regex import MatchesRegexFilter
from doodledashboard.notifications.outputs import ImageNotificationOutput
from doodledashboard.notifications.image.file_downloader import FileDownloader
from doodledashboard.notifications.notification import Notification


class ImageDependingOnMessageContent(Notification):
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

    def create_output(self, messages):
        if not messages:
            if self._default_image_path:
                return ImageNotificationOutput(self._default_image_path)
            else:
                return None

        last_message = messages[-1]

        for image_filter in self._filtered_images:
            if image_filter["filter"].filter(last_message):
                self._chosen_image_path = image_filter["path"]

        if self._chosen_image_path:
            image_path = self._chosen_image_path
        else:
            image_path = self._default_image_path

        return ImageNotificationOutput(image_path) if image_path else None

    @property
    def default_image(self):
        return self._default_image_path

    @property
    def filtered_images(self):
        return self._filtered_images

    def get_output_types(self):
        return [ImageNotificationOutput]

    def __str__(self):
        notification_name = "ImageDependingOnMessageContent"
        if self._name:
            notification_name += " (%s)" % self._name

        return notification_name


class ImageDependingOnMessageContentConfig(ComponentConfig, NotificationConfig):

    def __init__(self, file_downloader=FileDownloader()):
        super().__init__()
        self._file_downloader = file_downloader

    @staticmethod
    def get_id():
        return "image-depending-on-message-content"

    def create(self, options):
        notification = ImageDependingOnMessageContent()

        has_images = "images" in options
        has_default_image = "default-image" in options

        if not has_images and not has_default_image:
            raise MissingRequiredOptionException("Expected 'images' list and/or default-image to exist")

        if has_default_image:
            image_url = self._encode_url(options["default-image"])

            image_path = self.download(image_url)
            notification.add_image_filter(image_path)

        if has_images:
            for image_config_section in options["images"]:
                if "path" not in image_config_section:
                    raise MissingRequiredOptionException("Expected 'path' option to exist")

                image_url = self._encode_url(image_config_section["path"])

                image_filter = self._create_filter(image_config_section)
                image_path = self.download(image_url)

                notification.add_image_filter(image_path, image_filter)

        return notification

    def download(self, url):
        try:
            return self._file_downloader.download(url)
        except HTTPError as err:
            raise ComponentCreationException("Error '%s' when downloading %s" % (err.msg, err.url))

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
