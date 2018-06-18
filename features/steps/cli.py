from behave import given, when, then
from click.testing import CliRunner
from sure import expect

from doodledashboard.cli import view, start

_valid_cli_commands= {
    "start": start,
    "view": view
}


@given("I have the configuration called '{config_filename}'")
def _i_have_the_configuration_x(context, config_filename):
    if "dashboard_configs" not in context:
        context.dashboard_configs = {}

    context.dashboard_configs[config_filename] = context.text


@when("I call '{command} {arguments} {config_files}'")
def _i_call_x_x_config_yml(context, command, arguments, config_files):
    assert command in _valid_cli_commands.keys()
    cli_command = _valid_cli_commands.get(command)

    config_files = config_files.split(" ")
    arguments = arguments.split(" ")
    arguments += config_files

    runner = CliRunner()
    with runner.isolated_filesystem():
        for filename in config_files:
            if filename in context.dashboard_configs:
                with open(filename, "w") as f:
                    f.write(context.dashboard_configs[filename])


        context.runner_result = runner.invoke(cli_command, arguments, catch_exceptions=False)

@then('the output is')
def _the_output_is_x(context):
    cli_output = context.runner_result.output
    expect(cli_output).should_not.be.different_of(context.text)


@then('the status code is {code:d}')
def _the_status_code_is_x(context, code):
    cli_exit_code = context.runner_result.exit_code
    expect(cli_exit_code).should.equal(code)
