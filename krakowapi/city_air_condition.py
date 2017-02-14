import requests


class CityAirCondition:
    __URL = 'http://powietrze.malopolska.pl/_powietrzeapi/api/dane?act=danemiasta&ci_id=01'
    __CHECK_INTERVAL_S = 60 * 30
    __NEAREST_PM_2_5_ID = 1
    __NEAREST_PM_10_ID = 15

    __last_result_date = None

    def __init__(self):
        pass

    def read_data(self, clock_tick):
        if clock_tick % self.__CHECK_INTERVAL_S == 0:
            json_data = self.__make_request()
            return self.map_to_result(json_data)

    def __make_request(self):
        return requests.get(self.__URL).json()

    def map_to_result(self, json_data):
        pass


class Data:
    pass
