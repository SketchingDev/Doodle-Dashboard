from behave import given, when, then
from click.testing import CliRunner
from sure import expect

from doodledashboard.cli import view, start


@given("I have the configuration")
def _i_have_the_configuration_x(context):
    context.dashboard_config = context.text


@when("I call '{command} {arguments} config.yml'")
def _i_call_x_x_config_yml(context, command, arguments):
    commands = {"start": start, "view": view}
    assert command in commands.keys()

    arguments_split = arguments.split(" ")
    arguments_split.append("config.yml")

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("config.yml", "w") as f:
            f.write(context.dashboard_config)

        context.runner_result = runner.invoke(commands.get(command), arguments_split, catch_exceptions=False)


@then('the output is')
def _the_output_is_x(context):
    cli_output = context.runner_result.output
    expect(cli_output).should_not.be.different_of(context.text)


@then('the status code is {code:d}')
def _the_status_code_is_x(context, code):
    cli_exit_code = context.runner_result.exit_code
    expect(cli_exit_code).should.equal(code)
