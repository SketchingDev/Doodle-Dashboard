class MessageFilter:
    def __init__(self):
        self._next_filter = None

    def set_filter(self, filter):
        self._next_filter = filter

    def do_filter(self, messages):
        raise NotImplementedError('Implement this method')

    def filter(self, messages):
        filtered_messages = self.do_filter(messages)

        if self._next_filter:
            return self._next_filter.filter(filtered_messages)
        else:
            return filtered_messages


class MessageContainsTextFilter(MessageFilter):
    def __init__(self, text):
        MessageFilter.__init__(self)
        self._text = text

    def do_filter(self, messages):
        return [m for m in messages if self._text in m.get_text()]

    def remove_text(self, message):
        return message.get_text()\
            .replace(self._text, '')\
            .strip()


# class MessageMatchesRegexFilter(MessageFilter):
#     def __init__(self, regex):
#         MessageFilter.__init__(self)
#         self._regex = regex
#
#     def do_filter(self, messages):
#         matched_messages = []
#
#         for m in messages:
#             match = re.match(self._regex, m.get_text())
#             if match:
#                 matched_messages += m
#
#         return matched_messages




