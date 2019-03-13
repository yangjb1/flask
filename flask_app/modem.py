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

#cmdx="python new1.py"
#file to store complete telnet window content
#filename1=r"C:\Users\User\Desktop\mb\raw_log.txt"
#file to store only the latest telnet window content
#filename2=r"C:\Users\User\Desktop\mb\latest_raw_log.txt"
#file opened in append mode to keep previous data and append latest data to bottom
#file1=open(filename1,"a")
#file opened in write mode only to store latest content
#file2=open(filename2,"w")
try:
    #opening a telnet connection with host and port number, port and host could be modified in modem which might cause this program to fail
    tn = telnetlib.Telnet(HOST,2332)
    #read until 'login:' appears on telnet window
    tn.read_until(b"login: ")
    #after finding 'login' enter username, same process with password too
    tn.write(user.encode('ascii') + b"\n")
    #approx wait for 2 seconds for modem to authenticate username and print out 'password:'
    #time.sleep(2)
    #print("success0")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    #time.sleep(2)

    # Enter AT commands one after other with 1.5 sec wait time for modem to give command output
    tn.write(cmd0.encode('ascii')+b"\n")
    #time.sleep(1.5)
    tn.write(cmd4.encode('ascii')+b"\n")
    #time.sleep(1.5)
    tn.write(cmd1.encode('ascii')+b"\n")
    #time.sleep(1.5)
    tn.write(cmd2.encode('ascii')+b"\n")
    #time.sleep(1.5)
    tn.write(cmd3.encode('ascii')+b"\n")
    #time.sleep(1.5)
    tn.write(cmd5.encode('ascii')+b"\n")
    #time.sleep(1.5)
    tl1 =tn.read_very_eager().decode('ascii')
	#close telnet connection
    tn.close()
    #currentDT = datetime.datetime.now()
    #dtstr=str(currentDT)
	#Print date time along with telnet window content
    print (str(currentDT))
    print(tl1)
	#Write data to files and close
    #file1.write(str(currentDT))
    #file1.write(tl1)
    #file1.close()
    #file2.write(str(currentDT))
    #file2.write(tl1)
    #file2.close()
	#Call another program to process log text and save clean version to another file
    #os.system(cmdx)

except:
    print "ERROR"
    #In case of error at any point print 'Error' to text file
	#file1.write("Error")
	#file1.close()
	#file2.write("Error")
	#file2.close()
	#f2=open(r"C:\Users\User\Desktop\mb\a_clean_log.txt","a")
  #f3=open(r"C:\Users\User\Desktop\mb\w_clean_log.txt","w")
  #f2.write("Error")
  #f3.write("Error")
