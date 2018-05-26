# -- FILE: features/steps/example_steps.py
from behave import given, when, then


@given('we have behave installed')
def we_have_behave_installed(context):
    pass


@when('we implement {number:d} tests')
def we_implement_number_tests(context, number):  # -- NOTE: number is converted into integer
    assert number > 1 or number == 0
    context.tests_count = number


@then('behave will test them for us!')
def step_impl(context):
    assert context.failed is False
    assert context.tests_count >= 0
