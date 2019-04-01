import logging
import feedparser

from doodledashboard.component import DataFeedConfig, MissingRequiredOptionException, ComponentConfig
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class RssFeed(DataFeed):
    _COMMON_RSS_ITEM_FIELDS = ["title", "link", "description", "published", "id", "updated"]
    _SORT_ORDER = {
        "oldest": False,
        "newest": True
    }

    def __init__(self, url, sort_order=None):
        DataFeed.__init__(self)
        self._logger = logging.getLogger(__name__)
        self._feed_url = url
        self._sort_order = sort_order

    def get_url(self):
        return self._feed_url

    def get_sort_order(self):
        return self._sort_order

    def get_latest_messages(self):
        try:
            feed = feedparser.parse(self._feed_url)
        except RuntimeError as err:
            self._logger.error("Failed to download RSS feed for %s due to %s", self._feed_url, err)
            return []

        if self._sort_order:
            reverse = RssFeed._SORT_ORDER[self._sort_order]
            sorted_entries = sorted(feed.entries, key=lambda x: x["updated_parsed"], reverse=reverse)
        else:
            sorted_entries = feed.entries

        return [self._convert_to_message(entry) for entry in sorted_entries]

    def _convert_to_message(self, feed_item):
        feed_fields = []

        for field in RssFeed._COMMON_RSS_ITEM_FIELDS:
            if field in feed_item:
                feed_fields.append(feed_item[field])

        return Message("\n".join(feed_fields), self)

    def __str__(self):
        return "RSS feed for %s" % self._feed_url


class RssFeedConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "rss"

    def create(self, options):
        if "url" not in options:
            raise MissingRequiredOptionException("Expected 'url' option to exist")

        url = options["url"]
        sort_order = None
        if "sort" in options:
            if options["sort"] not in ["newest", "oldest"]:
                raise MissingRequiredOptionException(
                    "Sorting value for RSS feed can only be either ascending or descending"
                )

            sort_order = options["sort"]

        return RssFeed(url, sort_order)
