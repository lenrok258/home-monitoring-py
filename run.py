import os
import time

from pms5003 import PMS5003


def main():
    with PMS5003() as pms:
        while True:
            datas = pms.read_data()
            os.system('clear')
            print('\nBytes consumed:{}\n'.format(datas));
            print('\n======= PMS5003 ========\n'
                  'PM1.0(CF=1): {}\n'
                  'PM2.5(CF=1): {}\n'
                  'PM10 (CF=1): {}\n'
                  'PM1.0 (STD): {}\n'
                  '\033[93mPM2.5 (STD): {}\033[0m\n'
                  'PM10  (STD): {}\n'
                  '>0.3um     : {}\n'
                  '>0.5um     : {}\n'
                  '>1.0um     : {}\n'
                  '>2.5um     : {}\n'
                  '>5.0um     : {}\n'
                  '>10um      : {}\n'
                  'HCHO       : {}\n'.format(datas[0], datas[1], datas[2],
                                             datas[3], datas[4], datas[5],
                                             datas[6], datas[7], datas[8],
                                             datas[9], datas[10], datas[11],
                                             datas[12] / 1000.0))
            time.sleep(0.1)


if __name__ == '__main__':
    main()
