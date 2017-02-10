import time

import thingspeak
from pms5003.pms5003 import PMS5003


def main():
    clock_tick = 0
    with PMS5003() as pms:
        while True:
            pms_data = pms.read_data(clock_tick)
            print(pms_data)

            thingspeak.send_update(clock_tick, pms_data)

            time.sleep(1)
            clock_tick += 1


if __name__ == '__main__':
    main()
