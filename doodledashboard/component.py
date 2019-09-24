from abc import ABC, abstractmethod
from enum import Enum

from doodledashboard.datafeeds.datafeed import DataFeed
from doodledashboard.displays.display import Display
from doodledashboard.filters.filter import MessageFilter
from pkg_resources import iter_entry_points

from doodledashboard.notifications.notification import Notification


class NamedComponent(ABC):

    def __init__(self):
        self._name = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name


class ComponentCreator(ABC):
    """
    A factory that is inherited by components that create a component from a dashboard file.
    """

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def get_id() -> str:
        """
        :return: The ID for the component this factory can create
        """

    @abstractmethod
    def create(self, options: dict, secret_store: dict):
        """
        Creates the component from the options and secrets provided
        :param options: Components options
        :param secret_store: Storage for secrets
        :return: component
        """


class DisplayCreator(ComponentCreator):
    """
    This specific component interface is used by the component loader to determine that the implementor creates a
    display
    """

    @staticmethod
    @abstractmethod
    def get_id() -> str:
        """
        :return: The ID for the component this factory can create
        """

    @abstractmethod
    def create(self, options: dict, secret_store: dict) -> Display:
        """
        Creates the component from the options and secrets provided
        :param options: Components options
        :param secret_store: Storage for secrets
        :return: display
        """


class DataFeedCreator(ComponentCreator):
    """
    This specific component interface is used by the component loader to determine that the implementor creates a
    data-feed
    """

    @staticmethod
    @abstractmethod
    def get_id() -> str:
        """
        :return: The ID for the component this factory can create
        """

    @abstractmethod
    def create(self, options: dict, secret_store: dict) -> DataFeed:
        """
        Creates the component from the options and secrets provided
        :param options: Components options
        :param secret_store: Storage for secrets
        :return: Data-feed
        """


class FilterCreator:
    """
    This specific component interface is used by the component loader to determine that the implementor creates a
    filter
    """

    @staticmethod
    @abstractmethod
    def get_id() -> str:
        """
        :return: The ID for the component this factory can create
        """

    @abstractmethod
    def create(self, options: dict, secret_store: dict) -> MessageFilter:
        """
        Creates the component from the options and secrets provided
        :param options: Components options
        :param secret_store: Storage for secrets
        :return: filter
        """


class NotificationCreator:
    """
    This specific component interface is used by the component loader to determine that the implementor creates a
    notification
    """

    @staticmethod
    @abstractmethod
    def get_id() -> str:
        """
        :return: The ID for the component this factory can create
        """

    @abstractmethod
    def create(self, options: dict, secret_store: dict) -> Notification:
        """
        Creates the component from the options and secrets provided
        :param options: Components options
        :param secret_store: Storage for secrets
        :return: notification
        """


class ComponentCreationException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)

    @property
    def message(self):
        return self._message


class MissingRequiredOptionException(ComponentCreationException):
    def __init__(self, message):
        super().__init__(message)


class ComponentType(Enum):
    DISPLAY = 1
    DATA_FEED = 2
    NOTIFICATION = 3
    FILTER = 4


class ComponentCreatorLoader:

    def __init__(self):
        self._loaders = []

    def add_source(self, loader):
        self._loaders.append(loader)

    def load_by_type(self, component_type):
        component_creators = []

        for loader in self._loaders:
            component_creators += loader.load(component_type)

        return component_creators


class ComponentCreatorsSource(ABC):
    _COMPONENT_SUBCLASS_MAP = {
        ComponentType.DISPLAY: DisplayCreator,
        ComponentType.DATA_FEED: DataFeedCreator,
        ComponentType.FILTER: FilterCreator,
        ComponentType.NOTIFICATION: NotificationCreator
    }

    @abstractmethod
    def load(self, component_type):
        """
        Returns an array of all the component configs
        """

    def _filter_component_creators_by_type(self, classes, component_type):
        component_subclass = self._COMPONENT_SUBCLASS_MAP.get(component_type)

        filtered_components = filter(lambda c: issubclass(c, component_subclass), classes)
        return list(map(lambda c: c(), filtered_components))


class StaticComponentSource(ComponentCreatorsSource):
    _CREATORS = []

    @staticmethod
    def add(config):
        StaticComponentSource._CREATORS.append(config)

    def load(self, component_type):
        return self._filter_component_creators_by_type(
            StaticComponentSource._CREATORS,
            component_type
        )


class ExternalPackageSource(ComponentCreatorsSource):
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
        component_creators = self._find_entry_points_by_group(entry_point_name)

        return self._filter_component_creators_by_type(component_creators, component_type)
