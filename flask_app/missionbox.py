'''
# this is a library of functions will be using for the missionbox ui
# to use it in different python script
# first import file
# second call the function
'''
'''
# import filename as xx     # import
# xx.functionname           # calling function
'''

import os
import socket
import numpy as np
import cv2
import serial

#ser=serial.Serial('/dev/ttyACM0', 9600)
#gps=serial.Serial('/dev/ttyUSB0', 4800)
'''
TODO:
    -test gps
    -add modem status
'''
def shutdown():
    os.system('shutdown now -h')

def load_video(f):
    os.system('vlc ' + f)

def start_stream():
    os.system('ffserver')
    return

def stop_stream():
    os.system('pkill ffserver')
    return

def check_stream():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8090))
    if result==0:
        return True
    return False

def relay(x):
    ser.write(x)
    return

def status():
    line = ser.readline()
    line = line.split(',')
    return line

def gps():
    lines=gps.readline()
    line=lines.split(',')
    if line[0]=='$GPGGA':
        gps_data=line[2]+line[3]+','+line[4]+line[5]
        '''
        latitude=line[2]
        latDirec=line[3]
        longtitude=line[4]
        longDirec=line[5]
        '''
    return gps_data
