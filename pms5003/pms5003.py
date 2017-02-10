from struct import *

from config.config import config

if config['rpi-env']:
    import serial
    import RPi.GPIO as GPIO
else:
    import mocks.GPIO_mock as GPIO
    import mocks.serial_mock as serial

from pms5003_data import PMS5003Data


class PMS5003:
    __SET_GPIO_PIN = 0
    __SLEEP_DURATION_S = 1 * 5
    __ACTIVE_DURATION = 1 * 1

    port = None
    prev_data = None
    enabled = None

    def __init__(self):
        self.wake_up()

    def __enter__(self):
        self.port = self.__open_port()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print "Closing serial port..."
        if self.port is not None:
            self.port.close()
        print "Port closed"

    def read_data(self, clock_tick):
        self.__swith_on_off(clock_tick)
        data = self.__read_pm_line()
        self.port.flushInput()
        self.prev_data = data
        return data

    def __read_pm_line(self):
        rv = b''
        while True:
            ch1 = self.port.read()
            if ch1 == b'\x42':
                ch2 = self.port.read()
                if ch2 == b'\x4d':
                    rv += ch1 + ch2
                    rv += self.port.read(30)
                    line = rv[4:32]
                    data = unpack('>hhhhhhhhhhhhhh', line)
                    return PMS5003Data(data)

    def put_to_sleep(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__SET_GPIO_PIN, GPIO.OUT)
        GPIO.output(self.__SET_GPIO_PIN, GPIO.LOW)
        self.enabled = False

    def wake_up(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__SET_GPIO_PIN, GPIO.OUT)
        GPIO.output(self.__SET_GPIO_PIN, GPIO.HIGH)
        self.enabled = True

    def __open_port(self):
        print "Opening Serial Port...",
        port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=2.0)
        print "Serial Connected"
        return port

    def __swith_on_off(self, clock_tick):
        if self.enabled and (clock_tick % self.__ACTIVE_DURATION == 0):
            print "Putting to sleep {}, {}, {}".format(clock_tick, self.enabled, clock_tick % self.__ACTIVE_DURATION)
            self.put_to_sleep()
        if not self.enabled and (clock_tick % self.__SLEEP_DURATION_S == 0):
            print "Waking up {}, {}, {}".format(clock_tick, self.enabled, clock_tick % self.__SLEEP_DURATION_S)
        self.wake_up()
