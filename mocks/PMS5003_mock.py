class PMS5003:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read_data(self):
        return (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
