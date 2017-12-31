class MessageModel:
    def __init__(self, date, text):
        self._date = date
        self._text = text

    def get_date(self):
        return self._date

    def get_text(self):
        return self._text


class Repository:
    def __init__(self):
        pass

    def get_latest_messages(self):
        raise NotImplementedError('Implement this method')
