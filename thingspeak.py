import requests
import traceback

from config.config import config

__URL = "https://api.thingspeak.com/update"
__API_KEY = config['thingspeak']['write-api-key']
__IS_ENABLED = config['thingspeak']['enabled']
__REQUESTS_INTERVAL_SEC = config['thingspeak']['requests-interval-sec']


def send_update(clock_tick, pms_data):
    if not __IS_ENABLED or not __is_the_right_time(clock_tick):
        return

    __send_request(pms_data)


def __is_the_right_time(clock_tick):
    return clock_tick is not 0 \
           and clock_tick % __REQUESTS_INTERVAL_SEC == 0


def __send_request(pms_data):
    params_dict = {
        'api_key': __API_KEY,
        'field1': pms_data.pm1_atm,
        'field2': pms_data.pm2_5_atm,
        'field3': pms_data.pm10_atm}
    try:
        response = requests.post(__URL, params=params_dict)
    except Exception as e:
        print 'Sending to thingspeak.com failed. Exception:{}'.format(e)
    else:
        print 'Request sent to thingspeak.com. Response={}'.format(response)
