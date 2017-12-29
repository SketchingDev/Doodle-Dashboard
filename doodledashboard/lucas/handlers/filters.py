class MessageFilter:
    def __init__(self):
        pass

    def filter(self, messages):
        raise NotImplementedError('Implement this method')


class MessageContainsTextFilter(MessageFilter):
    def __init__(self, text):
        MessageFilter.__init__(self)
        self._text = text

    def filter(self, messages):
        return [m for m in messages if self._text in m.get_text()]

    def remove_text(self, message):
        return message.get_text()\
            .replace(self._text, '')\
            .strip()
