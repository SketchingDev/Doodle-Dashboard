from abc import ABC, abstractmethod
from enum import Enum
from pkg_resources import iter_entry_points


class ComponentConfig(ABC):
    """
    Inherited by components that can be defined and created from a dashboard file
    """

    @staticmethod
    @abstractmethod
    def get_id():
        """
        :return: Returns the ID used to represent the component in the config
        """

    @abstractmethod
    def create(self, options):
        """
        :param options: Element's options
        :return:
        """


class DisplayConfig:
    """
    Interface used to tell the component loader what type of component the implementor is.
    """


class DataFeedConfig:
    """
    Interface used to tell the component loader what type of component the implementor is.
    """


class FilterConfig:
    """
    Interface used to tell the component loader what type of component the implementor is.
    """


class NotificationConfig:
    """

    """


class ComponentCreationException(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class MissingRequiredOptionException(ComponentCreationException):
    def __init__(self, value):
        super().__init__(value)


class ComponentType(Enum):
    DISPLAY = 1
    DATA_FEED = 2
    NOTIFICATION = 3
    FILTER = 4


class ComponentConfigLoader:

    def __init__(self):
        self._loaders = []

    def add_source(self, loader):
        self._loaders.append(loader)

    def load_by_type(self, component_type):
        component_configs = []

        for loader in self._loaders:
            component_configs += loader.load(component_type)

        return component_configs


class ComponentConfigsSource(ABC):
    _COMPONENT_SUBCLASS_MAP = {
        ComponentType.DISPLAY: DisplayConfig,
        ComponentType.DATA_FEED: DataFeedConfig,
        ComponentType.FILTER: FilterConfig,
        ComponentType.NOTIFICATION: NotificationConfig
    }

    @abstractmethod
    def load(self, type):
        """
        Returns an array of all the component configs
        """

    def _filter_component_configs_by_type(self, classes, component_type):
        component_subclass = self._COMPONENT_SUBCLASS_MAP.get(component_type)

        # TODO use filter keyword to do filtering below
        filtered = []
        for component in classes:
            if issubclass(component, component_subclass):
                filtered.append(component())

        return filtered


class StaticComponentSource(ComponentConfigsSource):
    _CONFIGS = []

    @staticmethod
    def add(config):
        StaticComponentSource._CONFIGS.append(config)

    def load(self, component_type):
        return self._filter_component_configs_by_type(
            StaticComponentSource._CONFIGS,
            component_type
        )


class ExternalPackageSource(ComponentConfigsSource):
    _ENTRY_POINT_NAMES_MAP = {
        ComponentType.DISPLAY: "doodledashboard.custom.displays",
        ComponentType.DATA_FEED: "doodledashboard.custom.datafeeds",
        ComponentType.FILTER: "doodledashboard.custom.filters",
        ComponentType.NOTIFICATION: "doodledashboard.custom.notification"
    }

    @staticmethod
    def _find_entry_points_by_group(group_name):
        for entry_point in iter_entry_points(group_name):
            yield entry_point.load()

    def load(self, component_type):
        entry_point_name = self._ENTRY_POINT_NAMES_MAP.get(component_type)
        component_configs = self._find_entry_points_by_group(entry_point_name)

        return self._filter_component_configs_by_type(component_configs, component_type)
