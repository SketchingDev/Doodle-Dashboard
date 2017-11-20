from doodledashboard.lucas.handlers.handler import MessageHandler


class QuoteHandler(MessageHandler):
    _SAVED_VALUE_KEY = "QUOTE_HANDLER_LAST_KNOWN_QUOTE"

    def __init__(self, shelve):
        MessageHandler.__init__(self, shelve)

    def get_tag(self):
        return '#quote'

    def draw(self, display, messages):
        quote = self._extract_latest_quote(messages, '')

        if quote is '':
            if self.shelve.has_key(QuoteHandler._SAVED_VALUE_KEY):
                quote = self.shelve[QuoteHandler._SAVED_VALUE_KEY]
        else:
            self.shelve[QuoteHandler._SAVED_VALUE_KEY] = quote

        display.write_text(quote, 0, 0)
        display.flush()

    def _extract_latest_quote(self, messages, default):
        if not messages:
            return default
        else:
            text = messages[-1].get_text()
            return text.replace(self.get_tag(), '').strip()