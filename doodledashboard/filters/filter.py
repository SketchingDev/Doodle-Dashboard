from doodledashboard.configuration.config import Creator


class MessageFilter:
    def __init__(self):
        self._successor = None

    def add(self, successor):
        if not self._successor:
            self._successor = successor
        else:
            self._successor.add(successor)

    def do_filter(self, messages):
        return messages

    def filter(self, messages):
        filtered_messages = self.do_filter(messages)

        if self._successor:
            return self._successor.filter(filtered_messages)
        else:
            return filtered_messages


class FilterConfigCreator(Creator):
    def __init__(self):
        Creator.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError("Implement this method")

    def can_create(self, config_section):
        return "type" in config_section and self.creates_for_id(config_section["type"])

    def create_item(self, config_section):
        raise NotImplementedError("Implement this method")
