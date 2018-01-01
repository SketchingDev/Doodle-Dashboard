import feedparser
from dateutil import parser
from doodledashboard.lucas.datasources.repository import MessageModel, Repository


class RssFeed(Repository):
    def __init__(self, url):
        Repository.__init__(self)
        self._feed_url = url

    def get_latest_messages(self):
        feed = feedparser.parse(self._feed_url)
        return [self._convert_to_message(item) for item in feed['entries']]

    @staticmethod
    def _convert_to_message(feed_item):
        publish_date = parser.parse(feed_item['published'])
        title = feed_item['title']
        link = feed_item['link']
        summary = feed_item['summary']

        return MessageModel(publish_date, '%s \n %s \n %s' % (title, link, summary))
