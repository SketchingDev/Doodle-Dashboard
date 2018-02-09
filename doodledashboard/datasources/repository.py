from doodledashboard.config import Creator


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


class RepositoryConfigCreator(Creator):
    def __init__(self):
        Creator.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError('Implement this method')

    def can_create(self, config_section):
        return 'source' in config_section and self.creates_for_id(config_section['source'])

    def create_item(self, config_section):
        raise NotImplementedError('Implement this method')
