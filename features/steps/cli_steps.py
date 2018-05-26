from behave import given, when, then
from click.testing import CliRunner
from sure import expect

from doodledashboard.cli import view


@given("I have the configuration")
def _i_have_the_configuration_x(context):
    context.dashboard_config = context.text


@when("I call View with the type {action:w}")
def _run_cli_with_config(context, action):
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("config.yml", "w") as f:
            f.write(context.dashboard_config)

        context.runner_result = runner.invoke(view, [action, "config.yml"])


@then('the output is')
def _the_output_is_x(context):
    cli_output = context.runner_result.output
    expect(cli_output).should_not.be.different_of(context.text)


@then('the status code is {code:d}')
def _the_status_code_is_x(context, code):
    cli_exit_code = context.runner_result.exit_code
    expect(cli_exit_code).should.equal(code)
