import requests

from config.config import config

__URL = "https://api.thingspeak.com/update"
__API_KEY = ""


def send_update(pm_1, pm_2_5, pm_10):
    if not config['thingspeak']['enabled']:
        return

    params_dict = {
        'api_key': __API_KEY,
        'field1': pm_1,
        'field2': pm_2_5,
        'field3': pm_10}
    response = requests.post(__URL, params=params_dict)
    print response
