import unittest

from doodledashboard.lucas.datasources.rss import RssFeed


class TestRssFeedIT(unittest.TestCase):

    def test_real_rss_feed_parsed(self):
        repo = RssFeed('http://open.live.bbc.co.uk/weather/feeds/en/2643743/3dayforecast.rss')
        messages = repo.get_latest_messages()

        self.assertTrue(len(messages) > 0)


if __name__ == '__main__':
    unittest.main()
