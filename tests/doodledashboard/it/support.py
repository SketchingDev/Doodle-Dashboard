import unittest


class CliTestCase(unittest.TestCase):

    @staticmethod
    def save_file(filename, content):
        with open(filename, "w") as f:
            f.write(content)

    @staticmethod
    def call_cli(runner, cli_command, arguments=None):
        if arguments:
            arguments = arguments.split(" ")
        return runner.invoke(cli_command, arguments, catch_exceptions=False)
