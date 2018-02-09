import os
from os import path

from doodledashboard.handlers.handler import MessageHandler, MessageHandlerConfigCreator


class WeatherHandler(MessageHandler):
    _DEFAULT_KEY = 'cloudy'
    _SAVED_VALUE_KEY = "WEATHER_HANDLER_LAST_KNOWN_WEATHER"
    _SUN_FILENAME = "sun.bmp"
    _CLOUD_FILENAME = "cloud.bmp"
    _RAIN_FILENAME = "rain.bmp"
    _STORM_FILENAME = "storm.bmp"

    def __init__(self, key_value_store):
        MessageHandler.__init__(self, key_value_store)

        current_dir = WeatherHandler._get_current_directory()
        self._image_paths = {
            'sun': path.join(current_dir, WeatherHandler._SUN_FILENAME),
            'cloud': path.join(current_dir, WeatherHandler._CLOUD_FILENAME),
            'rain': path.join(current_dir, WeatherHandler._RAIN_FILENAME),
            'storm': path.join(current_dir, WeatherHandler._STORM_FILENAME)
        }

        if self.key_value_store.has_key(WeatherHandler._SAVED_VALUE_KEY):
            self._weather_key = self.key_value_store[WeatherHandler._SAVED_VALUE_KEY]
        else:
            self._weather_key = WeatherHandler._DEFAULT_KEY

    def update(self, messages):
        if messages:
            message_body = WeatherHandler._get_latest(messages) \
                .get_text() \
                .lower()

            for term in self._image_paths:
                if term in message_body:
                    self._weather_key = term
                    self.key_value_store[WeatherHandler._SAVED_VALUE_KEY] = term
                    return

    def draw(self, display):
        image_path = self._image_paths.get(self._weather_key)

        display.draw_image(image_path, 0, 0, display.get_size())
        display.flush()

    @staticmethod
    def _get_latest(messages):
        return messages[-1]

    @staticmethod
    def _get_current_directory():
        return os.path.dirname(os.path.realpath(__file__))


class WeatherMessageHandlerConfigCreator(MessageHandlerConfigCreator):
    def __init__(self, key_value_storage):
        MessageHandlerConfigCreator.__init__(self, key_value_storage)

    def create_handler(self, config_section, key_value_store):
        return WeatherHandler(key_value_store)

    def creates_for_id(self, filter_id):
        return filter_id == 'weather-handler'
