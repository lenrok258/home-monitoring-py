import os
import serial  
import time
from struct import *

print "Opening Serial Port...",
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=2.0)
print "Serial Connected"

def read_pm_line(_port):
    rv = b''
    while True:
        ch1 = _port.read()
        if ch1 == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(30)
                return rv

def main(): 
    cnt = 0
    while True:  
        recv = read_pm_line(ser)
        cnt = cnt + 1
        print "[%d]Recieve Data" % cnt,
        print len(recv), "Bytes:",
        tmp = recv[4:32]
        datas = unpack('>hhhhhhhhhhhhhh', tmp)
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
                                       datas[12]/1000.0))
        ser.flushInput()
        
        time.sleep(0.1)  


if __name__ == '__main__':  
    try:  
        main()  
    except KeyboardInterrupt:  
        if ser != None:  
            ser.close()
