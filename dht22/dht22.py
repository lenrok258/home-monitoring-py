import traceback

from config.config import config
from dht22_data import DHT22Data

if config['rpi-env']:
    import Adafruit_DHT as DHT22_sensor
else:
    import mocks.Adafruit_DHT_mock as DHT22_sensor


class DHT22:
    __RPI_GPIO_PIN = '27'
    __SENSOR_TYPE = DHT22_sensor.DHT22

    def __init__(self):
        pass

    def read(self):
        try:
            data_tuple = DHT22_sensor.read_retry(self.__SENSOR_TYPE, self.__RPI_GPIO_PIN)
            result = DHT22Data(data_tuple)
        except Exception as e:
            print 'Unable to fetch data from DHT22.\n Exception: {}'.format(e)
            traceback.print_exc()

        return result
