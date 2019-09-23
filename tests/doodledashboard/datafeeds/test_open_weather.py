import unittest
from unittest.mock import Mock
import pyowm

import pytest

from doodledashboard.component import MissingRequiredOptionException
from doodledashboard.datafeeds.open_weather import OpenWeatherCreator, OpenWeatherFeed
from doodledashboard.secrets_store import SecretNotFound


class TestConfig(unittest.TestCase):
    _EMPTY_OPTIONS = {}
    _EMPTY_SECRET_STORE = {}

    def test_id_is_open_weather(self):
        self.assertEqual("open-weather", OpenWeatherCreator.get_id())

    def test_exception_thrown_when_data_feed_created_with_empty_options(self):
        with pytest.raises(MissingRequiredOptionException) as err_info:
            OpenWeatherCreator().create(self._EMPTY_OPTIONS, self._EMPTY_SECRET_STORE)

        self.assertEqual("Expected 'place-name' or 'coords' option to exist", err_info.value.message)

    def test_exception_thrown_when_data_feed_created_with_empty_secret_store(self):
        with pytest.raises(SecretNotFound) as err_info:
            OpenWeatherCreator().create({"place-name": "London, GB"}, self._EMPTY_SECRET_STORE)

        self.assertEqual("Secret not found for ID 'open-weather-map-key'", err_info.value.message)


class TestFeed(unittest.TestCase):
    _EMPTY_OPTIONS = {}

    def test_feed_returns_date_and_time(self):
        weather = Mock()
        weather.get_status = Mock(return_value="test-status")
        weather.get_detailed_status = Mock(return_value="test-detailed-status")
        weather.get_temperature = Mock(return_value="test-temperature")

        observation = Mock()
        observation.get_weather = Mock(return_value=weather)

        weather_map_client = pyowm.OWM
        weather_map_client.weather_at_place = Mock(return_value=observation)

        data_feed = OpenWeatherFeed("London,GB", None, weather_map_client)
        data_feed.secret_store = {"open-weather-map-key": "test-token"}
        messages = data_feed.get_latest_messages()

        self.assertEqual(messages[0].text, 'test-detailed-status;test-status;test-temperature')


if __name__ == "__main__":
    unittest.main()
