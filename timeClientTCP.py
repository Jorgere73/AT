#!/usr/bin/python3

import sys
import socket
from datetime import datetime

SETENTA = 2208988800
#Represents the time in seconds equivalent to seventy years time


CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CSocket.connect(("utcnist.colorado.edu", 37))
#The default port to get time from a server is 37, specify in program arguments using -p if a different one is wanted
time = CSocket.recv(1024)
#The timestamp is given in bytes type
if time == None:
    print("TCP connection not working")
else:
    timestamp = int.from_bytes(time,"big") 
    #Converts the bytes pseudotimestamp into an integer using big endian order
    ahora = datetime.fromtimestamp((timestamp-SETENTA))
    formatdate = ahora.strftime("%a %b %d %H:%M:%S %Y")
    print(formatdate)
CSocket.close()