import logging


class MessageBroker:
    _handlers = []

    def __init__(self, display):
        self.display = display
        self.logger = logging.getLogger('raspberry_pi_dashboard.MessageBroker')

    def set_handlers(self, handlers):
        self._handlers = handlers

    def process(self, message):
        for handler in self._handlers:
            if handler.can_handle(message):
                self.logger.info("'%s' handling message: %s", handler.__class__, message)

                handler.handle(message, self.display)
                return handler

        return None
