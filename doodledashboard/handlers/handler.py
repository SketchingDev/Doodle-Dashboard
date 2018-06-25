from abc import ABC, abstractmethod

from doodledashboard.configuration.config import ConfigSection


class MessageHandler(ABC):
    """
    Abstract class for a message handler. Handlers are responsible for deciding what to display based on the messages
    they are given.

    Lifecycle:
        1. `initialise` is called when the dashboard is starting up. This is a great time to do intensive tasks
            like downloading images, to make the following phases as quick as possible.
        2. `update` is called with the message that the handler can use to decide what data to display
        3. `draw` is called when it is time to draw something to the display that was likely derived from the messages
            in the `update` phase
    """

    def __init__(self, key_value_store):
        self.key_value_store = key_value_store
        pass

    def initialise(self):
        pass

    @abstractmethod
    def update(self, text_entity):
        """
        This method is called with a message from the data feeds. It is within
        here that you decide what your handler will display when the draw method is called.
        """
        pass

    @abstractmethod
    def draw(self, display):
        pass

    @property
    @abstractmethod
    def display_requirements(self):
        return []

    def supports_display(self, display):
        for requirement in self.display_requirements:
            if not isinstance(display, requirement):
                return False

        return True


class MessageHandlerConfigSection(ConfigSection):
    """
    Abstract class for creating a MessageHandler from a dictionary structured like so:

        {
            handler: name-of-handler
        }
    """

    def __init__(self, key_value_store):
        ConfigSection.__init__(self)
        self._key_value_store = key_value_store

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def create_handler(self, config_section, key_value_store):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "handler" in config_section and self.creates_for_id(config_section["handler"])

    def create_item(self, config_section):
        return self.create_handler(config_section, self._key_value_store)
