from config.config import config

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
        return DHT22_sensor.read_retry(self.__SENSOR_TYPE, self.__RPI_GPIO_PIN)
