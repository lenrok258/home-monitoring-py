from struct import *

from config.config import config

if config['rpi-env']:
    import serial
    import RPi.GPIO as GPIO
else:
    import mocks.GPIO_mock as GPIO
    import mocks.serial_mock as serial

import pms5003_data


class PMS5003:
    __SET_GPIO_PIN = 0
    __SLEEP_DURATION_S = config['pms5003']['sleep-duration-sec']
    __ACTIVE_DURATION_S = config['pms5003']['active-duration-sec']

    __port = None
    __prev_data = None
    __sleeping = False

    def __init__(self):
        self.__wake_up()

    def __enter__(self):
        self.__port = self.__open_port()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print "Closing serial port..."
        if self.__port is not None:
            self.__port.close()
        print "Port closed"

    def read_data(self, clock_tick):
        self.__swith_on_off(clock_tick)

        if self.__sleeping:
            return self.__prev_data
        else:
            return self.__read_data_from_sensor()

    def __put_to_sleep(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__SET_GPIO_PIN, GPIO.OUT)
        GPIO.output(self.__SET_GPIO_PIN, GPIO.LOW)
        self.__sleeping = True

    def __wake_up(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__SET_GPIO_PIN, GPIO.OUT)
        GPIO.output(self.__SET_GPIO_PIN, GPIO.HIGH)
        self.__sleeping = False

    def __open_port(self):
        print "Opening Serial Port...",
        port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=2.0)
        print "Serial Connected"
        return port

    def __swith_on_off(self, clock_tick):
        cycle_duration = self.__SLEEP_DURATION_S + self.__ACTIVE_DURATION_S
        if clock_tick % cycle_duration == 0:
            print "Waking up. Clock tick: {}".format(clock_tick)
            self.__wake_up()
        elif clock_tick % cycle_duration == self.__ACTIVE_DURATION_S:
            print "Putting to sleep. Clock tick: {}".format(clock_tick)
            self.__wake_up()

    def __read_data_from_sensor(self):
        data = self.__read_pm_line()
        self.__port.flushInput()
        self.__prev_data = data
        return data

    def __read_pm_line(self):
        rv = b''
        while True:
            ch1 = self.__port.read()
            if ch1 == b'\x42':
                ch2 = self.__port.read()
                if ch2 == b'\x4d':
                    rv += ch1 + ch2
                    rv += self.__port.read(30)
                    line = rv[4:32]
                    data = unpack('>hhhhhhhhhhhhhh', line)
                    return pms5003_data.PMS5003Data(data)
