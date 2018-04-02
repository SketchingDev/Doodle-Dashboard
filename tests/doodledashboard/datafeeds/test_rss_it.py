import unittest

from doodledashboard.datasources.rss import RssFeed


class TestRssFeedIT(unittest.TestCase):

    def test_real_rss_feed_parsed(self):
        repo = RssFeed('https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/2643123')
        messages = repo.get_latest_messages()

        self.assertTrue(len(messages) > 0)


if __name__ == '__main__':
    unittest.main()
