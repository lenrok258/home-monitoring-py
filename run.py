import time

import requests.packages.urllib3

import thingspeak
from airly.airly_service import AirMeasurements as Airly
from pms5003.pms5003 import PMS5003

requests.packages.urllib3.disable_warnings()


def main():
    clock_tick = 0
    airly = Airly()

    with PMS5003() as pms:
        while True:
            pms_data = pms.read_data(clock_tick)
            print(pms_data)

            airly_data = airly.read()
            print(airly_data)

            thingspeak.send_update(clock_tick, pms_data)

            clock_tick += 1
            print '\n----------------\n'
            time.sleep(1)


if __name__ == '__main__':
    main()
