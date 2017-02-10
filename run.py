import os
import time

from pms5003.pms5003 import PMS5003


def main():
    clock_tick = 0
    with PMS5003() as pms:
        while True:
            data = pms.read_data(clock_tick)
            os.system('clear')
            print(data)
            # thingspeak.send_update(data[3], data[4], data[5])
            time.sleep(1)
            clock_tick += 1


if __name__ == '__main__':
    main()
