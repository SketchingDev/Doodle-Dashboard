class MessageHandler:
    def __init__(self, shelve):
        self.shelve = shelve
        pass

    def update(self, messages):
        raise NotImplementedError('Implement this method')

    def draw(self, display):
        raise NotImplementedError('Implement this method')
