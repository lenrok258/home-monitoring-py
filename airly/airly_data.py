def map_to_airly_result(result_dict):
    pm1 = result_dict['currentMeasurements']['pm1']
    pm2_5 = result_dict['currentMeasurements']['pm25']
    pm10 = result_dict['currentMeasurements']['pm10']
    temperature = result_dict['currentMeasurements']['temperature']
    return AirlyResult(pm1, pm2_5, pm10, temperature)


class AirlyResult:
    pm1 = None
    pm2_5 = None
    pm10 = None
    temperature = None

    def __init__(self, pm1, pm2_5, pm10, temperature):
        self.pm1 = int(pm1)
        self.pm2_5 = int(pm2_5)
        self.pm10 = int(pm10)
        self.temperature = round(temperature, 2)

    def __repr__(self):
        return "[AIRLY]: PM1.0: {}, PM2.5: {}, PM10: {}, Temperature: {}".format(self.pm1, self.pm2_5, self.pm10,
                                                                                 self.temperature)
