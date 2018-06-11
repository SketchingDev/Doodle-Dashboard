from behave import given

from doodledashboard.configuration.component_loaders import StaticDisplayLoader
from doodledashboard.displays.display import Display


@given("I load an external display")
def _i_have_the_configuration_x(context):
    StaticDisplayLoader.displays.append(TestDisplay)


class TestDisplay(Display):
    def clear(self):
        pass

    @staticmethod
    def get_id():
        return "test-display"

    def __str__(self):
        return self.get_id()
