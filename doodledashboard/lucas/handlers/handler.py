class MessageHandler:
    def __init__(self, shelve):
        self.shelve = shelve
        pass

    def draw(self, display, messages):
        raise NotImplementedError('Implement this method')

    def get_tag(self):
        raise NotImplementedError('Implement this method')
