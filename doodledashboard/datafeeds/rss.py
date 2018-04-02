import feedparser

from doodledashboard.config import MissingRequiredOptionException
from doodledashboard.datafeeds.repository import Repository, MessageModel, RepositoryConfigCreator


class RssFeed(Repository):
    def __init__(self, url):
        Repository.__init__(self)
        self._feed_url = url

    def get_url(self):
        return self._feed_url

    def get_latest_messages(self):
        feed = feedparser.parse(self._feed_url)
        return [self._convert_to_message(item) for item in feed['entries']]

    def __str__(self):
        return "RSS feed for %s" % self._feed_url

    @staticmethod
    def _convert_to_message(feed_item):
        title = feed_item['title']
        link = feed_item['link']
        summary = feed_item['summary']

        return MessageModel('%s \n %s \n %s' % (title, link, summary))


class RssFeedConfigCreator(RepositoryConfigCreator):
    def __init__(self):
        RepositoryConfigCreator.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == 'rss'

    def create_item(self, config_section):
        if 'url' not in config_section:
            raise MissingRequiredOptionException('Expected \'url\' option to exist')

        return RssFeed(config_section['url'])