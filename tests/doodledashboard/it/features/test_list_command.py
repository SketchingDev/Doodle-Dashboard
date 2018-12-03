import unittest

from click.testing import CliRunner

from doodledashboard.cli import list
from tests.doodledashboard.it.support import CliTestCase


class ListCommand(CliTestCase):

    def test_error_shown_if_component_type_not_recognised(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = self.call_cli(runner, list, "invalid-component-type")

        self.assertIn('Error: Invalid value for "component_type": invalid choice: invalid-component-type. (choose from',
                      result.output)
        self.assertEqual(2, result.exit_code)


if __name__ == '__main__':
    unittest.main()
