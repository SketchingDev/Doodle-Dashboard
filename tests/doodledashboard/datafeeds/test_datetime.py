import unittest
from click.testing import CliRunner
from mock import mock

from doodledashboard.cli import start


@mock.patch("time.sleep")
@mock.patch("itertools.cycle", side_effect=(lambda values: values))
@mock.patch("dbm.open") # Click uses file system isolation which breaks shelve when opening file
class TestCliStart(unittest.TestCase):

    def test_config_with_datetime_source_and_text_handler_prints_datetime(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config("""
            interval: 20
            display: console
            data-feeds:
              - source: datetime
            notifications:
              - title: Dummy Handler
                handler: text-handler
            """)

        last_line = result.output.splitlines()[-1]
        self.assertRegex(last_line, "\d{4}-\d{2}-\d{2} \d{2}:\d{2}")
        self.assertEqual(0, result.exit_code)

    @staticmethod
    def _run_cli_with_config(input_config):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("config.yml", "w") as f:
                f.write(input_config)

            return runner.invoke(start, ["config.yml"])


if __name__ == "__main__":
    unittest.main()
