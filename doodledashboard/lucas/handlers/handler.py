class MessageHandler:
    def __init__(self, shelve):
        self.shelve = shelve
        pass

    def draw(self, display, messages):
        raise NotImplementedError('Implement this method')

    def filter(self, messages):
        raise NotImplementedError('Implement this method')
