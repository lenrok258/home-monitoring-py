class PMS5003Data:
    pm1_std = None
    pm2_5_std = None
    pm10_std = None
    pm1_atm = None
    pm2_5_atm = None
    pm10_atm = None
    is_sleeping = False

    def __init__(self, data_list, is_sleeping):
        self.pm1_std = data_list[0]
        self.pm2_5_std = data_list[1]
        self.pm10_std = data_list[2]
        self.pm1_atm = data_list[3]
        self.pm2_5_atm = data_list[4]
        self.pm10_atm = data_list[5]
        self.is_sleeping = is_sleeping

    def __str__(self):
        return ('PMS5003: [CF=1]: PM1.0: {}, PM2.5: {}, PM10: {}, [Atmospheric]: PM1.0: {}, ' + \
                '\033[93mPM2.5: {}\033[0m, PM10: {}, isSleeping={}') \
            .format(self.pm1_std, self.pm2_5_std, self.pm10_std, self.pm1_atm,
                    self.pm2_5_atm, self.pm10_atm, self.is_sleeping)
