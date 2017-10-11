import time
import traceback
import locale

import requests.packages.urllib3

from airly.airly_service import AirMeasurements as Airly
from dht22.dht22 import DHT22
from lcd import display_20x4 as lcd
from pms5003.pms5003 import PMS5003
from thingspeak import data_sender as thingspeak
from logger import Logger

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
    logger = Logger('main')
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
                logger.info(pms_data)
            except Exception as e:
                logger.error("Unable to read PMS data: {}".format(e))
                traceback.print_exc()

            # try:
            #     airly_data = airly.read(clock_tick)
            #     logger.info(airly_data)
            # except Exception as e:
            #     logger.error("Unable to read AIRLY data: {}".format(e))
            #     traceback.print_exc()

            try:
                dht22_data = dht22.read()
                logger.info(dht22_data)
            except Exception as e:
                logger.error("Unable to read DHT22 data: {}".format(e))
                traceback.print_exc()

            try:
                fields = prepare_fields(pms_data, airly_data, dht22_data)
                thingspeak.send_update(clock_tick, fields)
            except Exception as e:
                logger.error("Unable to send data to THINGSPEAK: {}".format(e))
                traceback.print_exc()

            try:
                lcd.display(time.strftime("%d %b, %H:%M"), lcd.LINE_1, lcd.STYLE_ALIGN_CENTER)
                lcd.display('Temperatura: ' + str(dht22_data.temperature) + "*C", lcd.LINE_2, lcd.STYLE_ALIGN_CENTER)
                lcd.display('Wilgotnosc: ' + str(dht22_data.humidity) + "%", lcd.LINE_3, lcd.STYLE_ALIGN_CENTER)
                lcd.display('PM2.5: ' + str(pms_data.pm2_5_std) + "mg/dm3", lcd.LINE_4, lcd.STYLE_ALIGN_CENTER)
            except Exception as e:
                print "Unable to display data on LCD screen: {}".format(e)
                traceback.print_exc()

            clock_tick += 1
            logger.info('Clock tick: {}'.format(clock_tick))
            print '\n----------------\n'
            time.sleep(1)


if __name__ == '__main__':
    main()
