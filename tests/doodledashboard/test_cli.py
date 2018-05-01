import unittest

from click.testing import CliRunner
from mock import mock

from doodledashboard.cli import start


@mock.patch('time.sleep')
@mock.patch('itertools.cycle', side_effect=(lambda values: values))
@mock.patch('dbm.open') # Click uses file system isolation which breaks shelve when opening file
class TestCli(unittest.TestCase):
    """
    Click exception messages thrown by the program that aren't written to its output stream via click.echo
    """

    def test_invalid_yaml_in_config_prints_error_message(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config(':')

        self.assertIn("Error reading YAML in configuration file 'config.yml':", result.output)
        self.assertEqual(1, result.exit_code)

    def test_invalid_value_in_config_prints_error_message(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config('display: testing')

        self.assertEqual((
            'Missing value in your configuration:\n'
            "'Missing display option'\n"
            'Aborted!\n'),
            result.output
        )
        self.assertEqual(1, result.exit_code)

    def test_config_with_no_sources_nor_handlers_prints_info_about_none_being_loaded(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config('''
            interval: 10
            display: console
            ''')

        self.assertEqual((
            'Interval: 10\n'
            'Display loaded: Console display\n'
            '0 data sources loaded\n'
            '0 notifications loaded\n'),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_config_with_one_notification_prints_info_containing_datetime(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config('''
            interval: 20
            display: console
            data-feeds:
              - source: datetime
            ''')

        self.assertEqual((
            'Interval: 20\n'
            'Display loaded: Console display\n'
            '1 data sources loaded\n'
            ' - Date/Time (e.g. 2002-12-25T00:00)\n'
            '0 notifications loaded\n'),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_config_with_one_notification_prints_info_containing_notification(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config('''
            interval: 20
            display: console
            notifications:
              - title: Dummy Handler
                handler: text-handler
            ''')

        self.assertEqual((
            'Interval: 20\n'
            'Display loaded: Console display\n'
            '0 data sources loaded\n'
            '1 notifications loaded\n'
            ' - Displays messages using: Text handler\n\n'),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_config_with_datetime_source_and_text_handler_prints_datetime(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config('''
            interval: 20
            display: console
            data-feeds:
              - source: datetime
            notifications:
              - title: Dummy Handler
                handler: text-handler
            ''')

        last_line = result.output.splitlines()[-1]
        self.assertRegex(last_line, '\d{4}-\d{2}-\d{2}[A-Z]{1}\d{2}:\d{2}')
        self.assertEqual(0, result.exit_code)

    @staticmethod
    def _run_cli_with_config(input_config):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('config.yml', 'w') as f:
                f.write(input_config)

            return runner.invoke(start, ['config.yml'])


if __name__ == '__main__':
    unittest.main()
