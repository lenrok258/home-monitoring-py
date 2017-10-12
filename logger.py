from datetime import datetime


class Logger:

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def info(self, message):
        self.__print('INFO', message)

    def error(self, message):
        self.__print('ERROR', message)

    def warn(self, message):
        self.__print('WARN', message)

    def __print(self, level, message):
        nowString = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print '{0} [{1}] {2}: {3}'.format(nowString,
                                        level,
                                        self.tag_name,
                                        message)
