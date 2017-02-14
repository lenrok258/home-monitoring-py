import time

from pms5003.pms5003 import PMS5003


def main():
    with PMS5003() as pms:
        while True:
            pms_data = pms.read_data(0)
            print(pms_data)
            time.sleep(1)


if __name__ == '__main__':
    main()
