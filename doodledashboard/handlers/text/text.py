from doodledashboard.handlers.handler import MessageHandler, MessageHandlerConfigCreator


class TextHandler(MessageHandler):

    def __init__(self, key_value_store):
        MessageHandler.__init__(self, key_value_store)
        self._filtered_images = []
        self._text = ""

    def update(self, messages):
        self._text = "\n".join([m.get_text() for m in messages])

    def draw(self, display):
        display.write_text(self._text)

    def __str__(self):
        return "Text handler"


class TextHandlerConfigCreator(MessageHandlerConfigCreator):
    def __init__(self, key_value_storage):
        MessageHandlerConfigCreator.__init__(self, key_value_storage)

    def creates_for_id(self, filter_id):
        return filter_id == "text-handler"

    def create_handler(self, config_section, key_value_store):
        return TextHandler(key_value_store)
