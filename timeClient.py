#!/usr/bin/python3

import sys
import socket

CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CSocket.connect(("utcnist.colorado.edu", 37))
#The default port to get time from a server is 37, specify in program arguments using -p if a different one is wanted
time = CSocket.recv(1024)
if not time:
    print("TCP connection not working")
else:
    timeInt = int.from_bytes(time,"big")
    print(timeInt)
CSocket.close()