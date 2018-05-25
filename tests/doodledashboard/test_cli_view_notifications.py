import unittest
from click.testing import CliRunner
from mock import mock

from doodledashboard.cli import view


@mock.patch("time.sleep")
@mock.patch("itertools.cycle", side_effect=(lambda values: values))
@mock.patch("dbm.open")  # Click uses file system isolation which breaks shelve when opening file
class TestCliViewNotifications(unittest.TestCase):

    """
    Click exception messages thrown by the program aren't written to its output stream via click.echo
    """

    def test_one_message_shown_correctly(self, time_sleep, itertools_cycle, dbm_open):
        result = self._run_cli_with_config("""
            data-feeds:
              - source: text
                text:
                 - Hello
                 - Bob
              - source: text
                text: World
            notifications:
              - title: Display weather
                handler: text-handler
                filter-chain:
                  - type: message-matches-regex
                    pattern: (Hello)
             """)

        self.assertEqual((
            '{\n'
            '    "notifications": [\n'
            '        {\n'
            '            "filtered-data": [\n'
            '                {\n'
            '                    "source": "Text",\n'
            '                    "text": "Hello"\n'
            '                }\n'
            '            ],\n'
            '            "handler-actions": [\n'
            '                "Write text: \'Hello\'"\n'
            '            ],\n'
            '            "name": "Displays entities using: Text handler"\n'
            '        }\n'
            '    ],\n'
            '    "source-data": [\n'
            '        [\n'
            '            {\n'
            '                "source": "Text",\n'
            '                "text": "Hello"\n'
            '            },\n'
            '            {\n'
            '                "source": "Text",\n'
            '                "text": "Bob"\n'
            '            }\n'
            '        ],\n'
            '        [\n'
            '            {\n'
            '                "source": "Text",\n'
            '                "text": "World"\n'
            '            }\n'
            '        ]\n'
            '    ]\n'
            '}\n'),
            result.output
        )
        self.assertEqual(0, result.exit_code)

    @staticmethod
    def _run_cli_with_config(input_config):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("config.yml", "w") as f:
                f.write(input_config)

            return runner.invoke(view, ["notifications", "config.yml"])


if __name__ == "__main__":
    unittest.main()
