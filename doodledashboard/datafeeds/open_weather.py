import pyowm

from doodledashboard.component import MissingRequiredOptionException, DataFeedCreator
from doodledashboard.datafeeds.datafeed import DataFeed, Message
from doodledashboard.secrets_store import SecretNotFound


class GeoLocationOption:
    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    @staticmethod
    def _exists_and_is_numeric(option, key):
        if key not in option:
            raise MissingRequiredOptionException("Expected '%s' option to exist as part of location option" % key)
        elif not option[key].isnumeric():
            raise MissingRequiredOptionException("Expected '%s' option isn't numeric" % key)

        return option[key]

    @staticmethod
    def parse_option(position_option):
        latitude = GeoLocationOption._exists_and_is_numeric(position_option, "lat")
        longitude = GeoLocationOption._exists_and_is_numeric(position_option, "lon")

        return GeoLocationOption(latitude, longitude)

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude


class OpenWeatherFeed(DataFeed):

    def __init__(self, place_name, position, client):
        DataFeed.__init__(self)
        self._client = client

        self._place_name = place_name
        self._has_place_name = True if place_name else False

        self._position = position
        self._has_position = True if position else False

        if not self._has_place_name and not self._has_position:
            raise Exception("Place name or position has to be defined")

    def get_latest_messages(self):
        if self._has_position:
            observation = self._client.weather_at_coords(self._position.latitude, self._position.longitude)
        else:
            observation = self._client.weather_at_place(self._place_name)

        weather = observation.get_weather()

        detailed_status = weather.get_detailed_status()
        status = weather.get_status()
        temperature = weather.get_temperature(unit='celsius')
        message = "%s;%s;%s" % (detailed_status, status, temperature)

        return [Message(message)]

    def __str__(self):
        return "OpenWeather"


class OpenWeatherCreator(DataFeedCreator):
    _SECRET_TOKEN_ID = "open-weather-map-key"

    @staticmethod
    def get_id():
        return "open-weather"

    def create(self, options, secret_store):
        place_name = options["place-name"] if "place-name" in options else None
        coords = options["coords"] if "coords" in options else None

        if not place_name and not coords:
            raise MissingRequiredOptionException("Expected 'place-name' or 'coords' option to exist")

        owm_token = secret_store.get(self._SECRET_TOKEN_ID)
        if not owm_token:
            raise SecretNotFound(self, self._SECRET_TOKEN_ID)

        return OpenWeatherFeed(place_name, coords, pyowm.OWM(owm_token))
