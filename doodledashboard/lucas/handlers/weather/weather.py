import os
from os import path

from doodledashboard.lucas.handlers.filters import MessageContainsTextFilter
from doodledashboard.lucas.handlers.handler import MessageHandler


class WeatherHandler(MessageHandler):
    _DEFAULT_KEY = 'cloudy'
    _SAVED_VALUE_KEY = "WEATHER_HANDLER_LAST_KNOWN_WEATHER"
    _SUN_FILENAME = "sun.bmp"
    _CLOUD_FILENAME = "cloud.bmp"
    _RAIN_FILENAME = "rain.bmp"
    _STORM_FILENAME = "storm.bmp"

    def __init__(self, shelve):
        MessageHandler.__init__(self, shelve)

        current_dir = self._get_current_directory()
        self._message_filter = MessageContainsTextFilter('#weather')
        self._image_paths = {
            'sunny': path.join(current_dir, WeatherHandler._SUN_FILENAME),
            'cloudy': path.join(current_dir, WeatherHandler._CLOUD_FILENAME),
            'rainy': path.join(current_dir, WeatherHandler._RAIN_FILENAME),
            'stormy': path.join(current_dir, WeatherHandler._STORM_FILENAME)
        }

    def filter(self, messages):
        return self._message_filter.filter(messages)

    def draw(self, display, messages):
        weather = WeatherHandler._DEFAULT_KEY

        if not messages:
            if self.shelve.has_key(WeatherHandler._SAVED_VALUE_KEY):
                weather = self.shelve[WeatherHandler._SAVED_VALUE_KEY]
        else:
            new_weather = self._message_filter.remove_text(messages[-1])
            if self._image_paths.has_key(weather):
                weather = new_weather
                self.shelve[WeatherHandler._SAVED_VALUE_KEY] = weather

        image_path = self._image_paths.get(weather)

        display.draw_image(image_path, 0, 0, display.get_size())
        display.flush()

    def _get_current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))


