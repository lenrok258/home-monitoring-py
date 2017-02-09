from struct import *

import RPi.GPIO as GPIO
import serial


class PMS5003:
    __SET_GPIO_PIN = 0

    port = None

    def __init__(self):
        pass

    def __enter__(self):
        self.port = self.__open_port()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print "Closing serial port..."
        if self.port != None:
            self.port.close()
        print "Port closed"

    def read_data(self):
        recv = self.__read_pm_line()
        tmp = recv[4:32]
        datas = unpack('>hhhhhhhhhhhhhh', tmp)
        self.port.flushInput()
        return datas

    def __read_pm_line(self):
        rv = b''
        while True:
            ch1 = self.port.read()
            if ch1 == b'\x42':
                ch2 = self.port.read()
                if ch2 == b'\x4d':
                    rv += ch1 + ch2
                    rv += self.port.read(30)
                    return rv

    def put_to_sleep(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__SET_GPIO_PIN, GPIO.OUT)
        GPIO.output(self.__SET_GPIO_PIN, GPIO.LOW)

    def wake_up(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__SET_GPIO_PIN, GPIO.OUT)
        GPIO.output(self.__SET_GPIO_PIN, GPIO.HIGH)

    def __open_port(self):
        print "Opening Serial Port...",
        port = serial.Serial('/dev/ttyAMA0'(), baudrate=9600, timeout=2.0)
        print "Serial Connected"
        return port
