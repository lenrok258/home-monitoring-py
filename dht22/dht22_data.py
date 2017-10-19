class DHT22Data:
    temperature = None
    humidity = None

    def __init__(self, data_tuple):
        self.humidity = round(data_tuple[0], 2)
        self.temperature = round(data_tuple[1], 2)

    def __str__(self):
        return '[DHT22]: Humidity: {}%, Temperature: {}*C'.format(self.humidity, self.temperature);

