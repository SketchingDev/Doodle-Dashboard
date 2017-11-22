class MessageHandler:
    def __init__(self, shelve):
        self.shelve = shelve
        pass

    def draw(self, display, messages):
        raise NotImplementedError('Implement this method')

    def get_tag(self):
        raise NotImplementedError('Implement this method')

    def remove_tag(self, message):
        return message.get_text()\
            .replace(self.get_tag(), '')\
            .strip()