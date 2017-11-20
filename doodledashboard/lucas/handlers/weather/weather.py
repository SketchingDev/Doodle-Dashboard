import os
from os import path

from doodledashboard.lucas.handlers.handler import MessageHandler


class WeatherHandler(MessageHandler):
    _SAVED_VALUE_KEY = "WEATHER_HANDLER_LAST_KNOWN_WEATHER"
    _SUN_FILENAME = "sun.bmp"
    _CLOUD_FILENAME = "cloud.bmp"
    _RAIN_FILENAME = "rain.bmp"
    _STORM_FILENAME = "storm.bmp"

    def __init__(self, shelve):
        MessageHandler.__init__(self, shelve)

        current_dir = self._get_current_directory()
        self._image_paths = {
            'sun': path.join(current_dir, WeatherHandler._SUN_FILENAME),
            'cloud': path.join(current_dir, WeatherHandler._CLOUD_FILENAME),
            'rain': path.join(current_dir, WeatherHandler._RAIN_FILENAME),
            'storm': path.join(current_dir, WeatherHandler._STORM_FILENAME)
        }

    def get_tag(self):
        return '#weather'

    def draw(self, display, messages):
        weather = self._extract_weather(messages, '')

        if weather is '':
            if self.shelve.has_key(WeatherHandler._SAVED_VALUE_KEY):
                weather = self.shelve[WeatherHandler._SAVED_VALUE_KEY]
            else:
                weather = 'cloud'
        else:
            self.shelve[WeatherHandler._SAVED_VALUE_KEY] = weather

        if self._image_paths.has_key(weather):
            image_path = self._image_paths.get(weather)
        else:
            image_path = self._image_paths.get('cloud')

        display.draw_image(image_path, 0, 0, display.get_size())
        display.flush()

    def _get_current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def _extract_weather(self, messages, default):
        if not messages:
            return default
        else:
            text = messages[-1].get_text()
            return text.replace(self.get_tag(), '').strip()
