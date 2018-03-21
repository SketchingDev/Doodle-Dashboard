from doodledashboard.config import Creator


class Display:
    def __init__(self):
        pass

    def clear(self):
        raise NotImplementedError('Implement this method')

    def write_text(self, text, x, y, font_size=10, font_face=None):
        raise NotImplementedError('Implement this method')

    def draw_image(self, image_path, x, y, size):
        raise NotImplementedError('Implement this method')

    def flush(self):
        raise NotImplementedError('Implement this method')

    def get_size(self):
        raise NotImplementedError('Implement this method')


class DisplayConfigCreator(Creator):
    def __init__(self):
        Creator.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError('Implement this method')

    def can_create(self, config_section):
        return 'display' in config_section and self.creates_for_id(config_section['display'])

    def create_item(self, config_section):
        raise NotImplementedError('Implement this method')
