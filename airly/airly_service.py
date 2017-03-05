import requests

import airly_data
from config.config import config


class AirMeasurements:
    __URL_TEMPLATE = "https://airapi.airly.eu/v1/mapPoint/measurements?latitude={}&longitude={}"
    __API_KEY_HEADER_NAME = "apikey"

    url = None
    api_key = None

    def __init__(self):
        latitude = config['airly']['location']['latitude']
        longitude = config['airly']['location']['longitude']
        self.url = self.__URL_TEMPLATE.format(latitude, longitude)
        self.api_key = config['airly']['api-key']

    def read(self):
        response = requests.get(self.url, headers={self.__API_KEY_HEADER_NAME: self.api_key})
        result_dict = response.json()
        return airly_data.map_to_airly_result(result_dict)


if __name__ == '__main__':
    print AirMeasurements().read()
