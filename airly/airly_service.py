import requests

import airly_data
from config.config import config


class AirMeasurements:
    __URL_TEMPLATE = "https://airapi.airly.eu/v1/mapPoint/measurements?latitude={}&longitude={}"
    __API_KEY_HEADER_NAME = "apikey"
    __REQUESTS_INTERVAL_SEC = 60

    url = None
    api_key = None
    previous = None

    def __init__(self):
        latitude = config['airly']['location']['latitude']
        longitude = config['airly']['location']['longitude']
        self.url = self.__URL_TEMPLATE.format(latitude, longitude)
        self.api_key = config['airly']['api-key']

    def read(self, clock_tick):
        if clock_tick % self.__REQUESTS_INTERVAL_SEC != 0:
            return self.previous

        print "Sending request to AIRLY"
        response = requests.get(self.url, headers={self.__API_KEY_HEADER_NAME: self.api_key})
        result_dict = response.json()
        result = airly_data.map_to_airly_result(result_dict)
        self.previous = response
        return result


if __name__ == '__main__':
    print AirMeasurements().read()
