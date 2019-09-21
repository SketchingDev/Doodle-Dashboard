from doodledashboard.component import MissingRequiredOptionException, DataFeedConfig, ComponentConfig
from doodledashboard.datafeeds.datafeed import DataFeed, Message
import pyowm

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
    _SECRET_TOKEN_ID = "open-weather-map-key"

    def __init__(self, place_name, position, client_creator=lambda token: pyowm.OWM(token)):
        DataFeed.__init__(self)
        self._client = None
        self._client_creator = client_creator

        self._place_name = place_name
        self._has_place_name = True if place_name else False

        self._position = position
        self._has_position = True if position else False

        if not self._has_place_name and not self._has_position:
            raise Exception("Place name or position has to be defined")

    def _create_client(self):
        # @todo Update Secret store to make easy to try and get secret else throw exception asking for it
        # @body By passing the secrets into the Config it will allow the client to be injected into the DataFeed making
        #       testing easier
        owm_token = self.secret_store.get(self._SECRET_TOKEN_ID)
        if owm_token:
            return self._client_creator(owm_token)
        else:
            raise SecretNotFound(self, self._SECRET_TOKEN_ID)

    def get_latest_messages(self):
        if not self._client:
            self._client = self._create_client()

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


class OpenWeatherConfig(ComponentConfig, DataFeedConfig):

    @staticmethod
    def get_id():
        return "open-weather"

    def create(self, options):
        place_name = options["place-name"] if "place-name" in options else None
        coords = options["coords"] if "coords" in options else None

        if not place_name and not coords:
            raise MissingRequiredOptionException("Expected 'place-name' or 'coords' option to exist")

        return OpenWeatherFeed(place_name, coords)
