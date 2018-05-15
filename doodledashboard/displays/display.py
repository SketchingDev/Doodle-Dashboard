from doodledashboard.configuration.config import ConfigSection


class Display:
    # TODO Provide way to say what operations the display supports

    def __init__(self):
        pass

    def clear(self):
        raise NotImplementedError("Implement this method")

    def write_text(self, text, font_face=None):
        raise NotImplementedError("Implement this method")

    def draw_image(self, image_path):
        raise NotImplementedError("Implement this method")

    def fill_colour(self, colour):
        raise NotImplementedError("Implement this method")


class DisplayConfigSection(ConfigSection):
    def __init__(self):
        ConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "display" in config_section and self.creates_for_id(config_section["display"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")
