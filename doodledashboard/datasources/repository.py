class MessageModel:
    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text


class Repository:
    def __init__(self):
        pass

    def get_latest_messages(self):
        raise NotImplementedError('Implement this method')
