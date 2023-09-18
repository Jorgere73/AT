#!/usr/bin/python3

import sys
import socket
from datetime import date, time

CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CSocket.connect(("utcnist.colorado.edu", 37))
#The default port to get time from a server is 37, specify in program arguments using -p if a different one is wanted
time = CSocket.recv(1024)
if time == None:
    print("TCP connection not working")
else:
    timestamp = int.from_bytes(time,"big")
    print(timestamp)
    ahora = date.fromtimestamp((timestamp-2208988800))
    
    formatdate = ahora.strftime("%a %b %d {0}:%M:%S %Y".format(ahora.hour))
    print(formatdate)
CSocket.close()