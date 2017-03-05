import time
import traceback

import requests.packages.urllib3

from airly.airly_service import AirMeasurements as Airly
from dht22.dht22 import DHT22
from pms5003.pms5003 import PMS5003
from thingspeak import data_sender as thingspeak

requests.packages.urllib3.disable_warnings()


def prepare_fields(pms_data, airly_data, dht22_data):
    return [
        getattr(pms_data, 'pm1_atm', ''),
        getattr(pms_data, 'pm2_5_atm', ''),
        getattr(pms_data, 'pm10_atm', ''),
        getattr(dht22_data, 'humidity', ''),
        getattr(dht22_data, 'temperature', ''),
        getattr(airly_data, 'pm2_5', ''),
        getattr(airly_data, 'pm10', ''),
        getattr(airly_data, 'temperature', '')
    ]


def main():
    clock_tick = 0
    airly = Airly()
    dht22 = DHT22()

    with PMS5003() as pms:
        while True:
            pms_data = None
            airly_data = None
            dht22_data = None

            try:
                pms_data = pms.read_data(clock_tick)
                print(pms_data)
            except Exception as e:
                print "Unable to read PMS data: {}".format(e)
                traceback.print_exc()

            try:
                airly_data = airly.read()
                print(airly_data)
            except Exception as e:
                print "Unable to read AIRLY data: {}".format(e)
                traceback.print_exc()

            try:
                dht22_data = dht22.read()
                print (dht22_data)
            except Exception as e:
                print "Unable to read DHT22 data: {}".format(e)
                traceback.print_exc()

            try:
                fields = prepare_fields(pms_data, airly_data, dht22_data)
                thingspeak.send_update(clock_tick, fields)
            except Exception as e:
                print "Unable to send data to THINGSPEAK: {}".format(e)
                traceback.print_exc()

            clock_tick += 1
            print '\n----------------\n'
            time.sleep(1)


if __name__ == '__main__':
    main()
