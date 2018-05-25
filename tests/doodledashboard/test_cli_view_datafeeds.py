import unittest
from click.testing import CliRunner
from mock import mock

from doodledashboard.cli import view


@mock.patch("time.sleep")
@mock.patch("itertools.cycle", side_effect=(lambda values: values))
@mock.patch("dbm.open")  # Click uses file system isolation which breaks shelve when opening file
class TestCliViewDataFeeds(unittest.TestCase):
    """
    Click exception messages thrown by the program aren't written to its output stream via click.echo
    """

    def test_one_message_shown_correctly(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config("""
                    data-feeds:
                        - source: text
                          text: Hello World
                    """)

        self.assertEqual((
            "{\n"
            '    "source-data": [\n'
            "        [\n"
            "            {\n"
            '                "source": "Text",\n'
            '                "text": "Hello World"\n'
            "            }\n"
            "        ]\n"
            "    ]\n"
            "}\n"),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    def test_two_messages_shown_correctly(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config("""
            data-feeds:
                - source: text
                  text:
                    - Hello
                    - World
            """)

        self.assertEqual((
            "{\n"
            '    "source-data": [\n'
            "        [\n"
            "            {\n"
            '                "source": "Text",\n'
            '                "text": "Hello"\n'
            "            },\n"
            "            {\n"
            '                "source": "Text",\n'
            '                "text": "World"\n'
            "            }\n"
            "        ]\n"
            "    ]\n"
            "}\n"),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @staticmethod
    def _run_cli_with_config(input_config):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("config.yml", "w") as f:
                f.write(input_config)

            return runner.invoke(view, ["datafeeds", "config.yml"])


if __name__ == "__main__":
    unittest.main()
