import logging
import unittest

import pytest
from click.testing import CliRunner
from mock import mock
from pytest_localserver import http

from doodledashboard.cli import view


@pytest.mark.usefixtures
@mock.patch('time.sleep')
@mock.patch('itertools.cycle', side_effect=(lambda values: values))
@mock.patch('dbm.open')  # Click uses file system isolation which breaks shelve when opening file
class TestCliView(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server = http.ContentServer()
        server.start()

        TestCliView.disable_localserver_logging()

        cls.http_server = server

    @classmethod
    def tearDownClass(cls):
        cls.http_server.stop()

    """
    Click exception messages thrown by the program that aren't written to its output stream via click.echo
    """

    def test_datetime_datafeed_in_config_produces_output_from_feed(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config('''
            data-feeds:
              - source: datetime
            ''')

        self.assertIn((
            'Date/Time (e.g. 2002-12-25T00:00) --------------\n'
            'Message:\n'),
            result.output
        )
        last_line = result.output.splitlines()[-1]
        self.assertRegex(last_line, '\d{4}-\d{2}-\d{2}[A-Z]{1}\d{2}:\d{2}')

        self.assertEqual(0, result.exit_code)

    def test_rss_datafeed_in_config_produces_output_from_feed(self, time_sleep, itertools_cycle, dbm_open):
        feed = \
            '<?xml version="1.0" encoding="UTF-8"?>\
            <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\
              <channel>\
                <title>Example RSS Feed</title>\
                <link>https://exmaple/rss/feed/</link>\
                <description>Example RSS feed used for tests</description>\
                <item>\
                  <title>Dummy Item 1</title>\
                  <link>https://dummy-link/1</link>\
                  <description>Desc for 1</description>\
                </item>\
                <item>\
                  <title>Dummy Item 2</title>\
                  <link>https://dummy-link/2</link>\
                  <description>Desc for 2</description>\
                </item>\
              </channel>\
            </rss>'

        self.http_server.serve_content(feed)

        result = self._run_cli_with_config('''
            data-feeds:
                - source: rss
                  url: %s
            ''' % self.http_server.url)

        self.assertEqual((
            f'RSS feed for {self.http_server.url} --------------\n'
            'Message:\n'
            'Dummy Item 1\n'
            'https://dummy-link/1\n'
            'Desc for 1\n'
            'Message:\n'
            'Dummy Item 2\n'
            'https://dummy-link/2\n'
            'Desc for 2\n'),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @staticmethod
    def _run_cli_with_config(input_config):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('config.yml', 'w') as f:
                f.write(input_config)

            return runner.invoke(view, ['datafeeds', 'config.yml'])

    @staticmethod
    def disable_localserver_logging():
        """
        pytest_localserver uses Werkzeug, a WSGI utility library, which outputs logs
        which interfere with asserting the output of the CLI
        """
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)


if __name__ == '__main__':
    unittest.main()
