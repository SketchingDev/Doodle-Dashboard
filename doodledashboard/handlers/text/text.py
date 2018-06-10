from doodledashboard.handlers.handler import MessageHandler, MessageHandlerConfigSection


class TextHandler(MessageHandler):

    def supports_display(self, display):
        pass

    def __init__(self, key_value_store):
        MessageHandler.__init__(self, key_value_store)
        self._filtered_images = []
        self._text = ""

    def update(self, text_entity):
        self._text = text_entity.get_text()

    def draw(self, display):
        display.write_text(self._text)

    def __str__(self):
        return "Text handler"


class TextHandlerConfigCreator(MessageHandlerConfigSection):
    def __init__(self, key_value_storage):
        MessageHandlerConfigSection.__init__(self, key_value_storage)

    def creates_for_id(self, filter_id):
        return filter_id == "text-handler"

    def create_handler(self, config_section, key_value_store):
        return TextHandler(key_value_store)
