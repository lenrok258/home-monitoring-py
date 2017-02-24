import time

import requests.packages.urllib3

from airly.airly_service import AirMeasurements as Airly
from dht22.dht22 import DHT22
from pms5003.pms5003 import PMS5003
from thingspeak import data_sender as thingspeak

requests.packages.urllib3.disable_warnings()


def prepare_fields(pms_data, airly_data, dht22_data):
    return [
        pms_data.pm1_atm,
        pms_data.pm2_5_atm,
        pms_data.pm10_atm,
        dht22_data.humidity,
        dht22_data.temperature,
        airly_data.pm2_5,
        airly_data.pm10,
        airly_data.temperature
    ]


def main():
    clock_tick = 0
    airly = Airly()
    dht22 = DHT22()

    with PMS5003() as pms:
        while True:
            try:
                pms_data = pms.read_data(clock_tick)
                print(pms_data)

                airly_data = airly.read()
                print(airly_data)

                dht22_data = dht22.read()
                print (dht22_data)

                fields = prepare_fields(pms_data, airly_data, dht22_data)
                thingspeak.send_update(clock_tick, fields)

                clock_tick += 1
                print '\n----------------\n'
                time.sleep(1)
            except Exception as e:
                print "Exception cought: {}".format(e)


if __name__ == '__main__':
    main()
