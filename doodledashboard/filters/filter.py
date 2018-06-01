from doodledashboard.configuration.config import ConfigSection


class TextEntityFilter:
    def __init__(self):
        self._successor = None

    def filter(self, text_entity):
        raise NotImplementedError("Implement this method")


class FilterConfigSection(ConfigSection):
    def __init__(self):
        ConfigSection.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "type" in config_section and self.creates_for_id(config_section["type"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")
