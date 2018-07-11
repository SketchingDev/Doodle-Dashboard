import feedparser

from doodledashboard.configuration.config import MissingRequiredOptionException, ConfigSection
from doodledashboard.datafeeds.datafeed import DataFeed, Message


class RssFeed(DataFeed):
    _COMMON_RSS_ITEM_FIELDS = ["title", "link", "description", "published", "id", "updated"]
    _SORT_ORDER = {
        "oldest": False,
        "newest": True
    }

    def __init__(self, url, sort_order=None):
        DataFeed.__init__(self)
        self._feed_url = url
        self._sort_order = sort_order

    def get_url(self):
        return self._feed_url

    def get_sort_order(self):
        return self._sort_order

    def get_latest_messages(self):
        feed = feedparser.parse(self._feed_url)

        if self._sort_order:
            reverse = RssFeed._SORT_ORDER[self._sort_order]
            sorted_entries = sorted(feed.entries, key=lambda x: x["updated_parsed"], reverse=reverse)
        else:
            sorted_entries = feed.entries

        return [self._convert_to_message(entry) for entry in sorted_entries]

    def __str__(self):
        return "RSS feed for %s" % self._feed_url

    def _convert_to_message(self, feed_item):
        feed_fields = []

        for field in RssFeed._COMMON_RSS_ITEM_FIELDS:
            if field in feed_item:
                feed_fields.append(feed_item[field])

        return Message("\n".join(feed_fields), self)

    @staticmethod
    def get_config_factory():
        return RssFeedConfig()


class RssFeedConfig(ConfigSection):

    @property
    def id_key_value(self):
        return "source", "rss"

    def create(self, config_section):
        if "url" not in config_section:
            raise MissingRequiredOptionException("Expected 'url' option to exist")

        url = config_section["url"]
        sort_order = None
        if "sort" in config_section:
            if config_section["sort"] not in ["newest", "oldest"]:
                raise MissingRequiredOptionException(
                    "Sorting value for RSS feed can only be either ascending or descending"
                )

            sort_order = config_section["sort"]

        return RssFeed(url, sort_order)
