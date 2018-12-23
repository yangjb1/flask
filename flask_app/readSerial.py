#!/usr/bin/python
import serial
import time


ser = serial.Serial('/dev/ttyACM0', 9600)
f = open("meter",'w')
f.write(ser.readline())
f.close()
time.sleep(10)
#
    #f.flush()
