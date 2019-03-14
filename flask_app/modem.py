#!/usr/bin/python
import getpass
import sys
import telnetlib
import time
import datetime
import os
import math

HOST = "192.168.13.31"
user = "user"
password = "missionbox"
cmd0="AT*NETIP?"
cmd1="AT*NETSTATE?"
cmd2="AT*LTERSRQ?"
cmd3="AT*NETRSSI?"
cmd4="AT*NETSERV?"
cmd5="AT*GPSDATA?"
def modem():
  try:
    tn = telnetlib.Telnet(HOST,2332)
    tn.read_until(b"login: ")
    tn.write(user + b"\n")
    #time.sleep(2)
    tn.read_until(b"Password: ")
    tn.write(password + b"\n")
    time.sleep(1)

    tn.write(cmd0+b"\n")
    time.sleep(1)
    tn.write(cmd4+b"\n")
    time.sleep(1)
    tn.write(cmd1+b"\n")
    time.sleep(1)
    tn.write(cmd2+b"\n")
    time.sleep(1)
    tn.write(cmd3+b"\n")
    time.sleep(1)
    tn.write(cmd5+b"\n")
    time.sleep(1)
    tl1 = ''
    tl1 = tn.read_very_eager()
	  #close telnet connection
    tn.close()
    print tl1

    ttl = tl1.split()
    print ttl
    #ttl = list(filter(None, ttl))

    temp = ''
    for i in range(0,len(ttl)):
      if ttl[i] == cmd0:
        temp = temp + ttl[i+1] + ','
      if ttl[i] == cmd1:
          if ttl[i+2] is not 'Ready':
              temp += 'Down,'
      if ttl[i] == cmd2:
        temp = temp + ttl[i+1] + ','
      if ttl[i] == cmd3:
        temp = temp + ttl[i+1] + ','
      if ttl[i] == cmd4:
        temp = temp + ttl[i+1] + ','
      if ttl[i] == cmd5:
        x = ttl[i+2]
        temp += x[4:] + ','
        x = ttl[i+4]
        temp += x[6:] + ','
        x = ttl[i+5]
        temp += x[9:] + ','
        x = ttl[i+6]
        temp += x[10:]

    #print temp
    return temp
  except:
    print "ERROR"
    return 'error'
