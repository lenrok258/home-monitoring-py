import traceback

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
        try:
            response = requests.get(self.url, headers={self.__API_KEY_HEADER_NAME: self.api_key})
            result_dict = response.json()
            result = airly_data.map_to_airly_result(result_dict)
        except Exception as e:
            print 'Unable to fetch data from Airly.\n Exception: {}'.format(e)
            traceback.print_exc()

        return result


if __name__ == '__main__':
    print AirMeasurements().read()
