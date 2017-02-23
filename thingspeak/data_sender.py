from config.config import config
import requests

__URL = "https://api.thingspeak.com/update"
__API_KEY = config['thingspeak']['write-api-key']
__IS_ENABLED = config['thingspeak']['enabled']
__REQUESTS_INTERVAL_SEC = config['thingspeak']['requests-interval-sec']


def send_update(clock_tick, fields):
    if not __IS_ENABLED or not __is_the_right_time(clock_tick):
        return

    __send_request(fields)


def __is_the_right_time(clock_tick):
    return clock_tick is not 0 \
           and clock_tick % __REQUESTS_INTERVAL_SEC == 0


def __send_request(fields):
    params_dict = {
        'api_key': __API_KEY,
    }

    for (i, field) in enumerate(fields):
        key = 'field' + str(i + 1)
        params_dict[key] = field

    try:
        response = requests.post(__URL, params=params_dict)
    except Exception as e:
        print 'Sending to thingspeak.com failed. Exception:{}'.format(e)
    else:
        print 'Request sent to thingspeak.com. Response={}'.format(response)
