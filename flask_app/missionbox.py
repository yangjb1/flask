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
import urllib2

ser=serial.Serial('/dev/ttyACM0', 9600)
#gps=serial.Serial('/dev/ttyUSB0', 4800)

'''
TODO:
    -test gps
    -add modem status
'''

def ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def shutdown():
    os.system('shutdown now -h')

def load_video(f):
    os.system('vlc static/' + f)

def start_stream():
    os.system('ffserver')
    return

def stop_stream():
    os.system('pkill ffserver')
    return

def check_modem():
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('192.168.13.31', 9191))
    if result == 0:
        return 'True'
    return 'False'
    '''
    try:
        urlib2.urlopen('http://localhost:8090', timeout=1)
        return 'True'
    except urllib2.URLError as err:
        return 'False'
    '''

def check_stream():
    #socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8090))
    if result == 0:
        return True
    return False

def reset():
    ser.write('0')
    return

def relay(x):
    ser.write(x)
    return

def status():
    line = ser.readline()
    #line = line.split(',')
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
