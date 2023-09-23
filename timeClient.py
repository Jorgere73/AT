#!/usr/bin/python3

import sys
import socket
from datetime import datetime

SETENTA = 2208988800
#Represents the time in seconds equivalent to seventy years time


def formatDate(input):
    timestamp = int.from_bytes(input,"big") 
    #Converts the bytes pseudotimestamp into an integer using big endian order
    ahora = datetime.fromtimestamp((timestamp-SETENTA))
    formatdate = ahora.strftime("%a %b %d %H:%M:%S %Y")
    print(formatdate)

def clientMode(mode, servername, port = 37):
    if(servername == ""):
        print("Server name not specified, set using -s")
        sys.exit()
    if(mode == "tcp"):
        try:
            CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CSocket.connect((serverName, port))
            
            #The default port to get time from a server is 37, specify in program arguments using -p if a different one is wanted
            time = CSocket.recv(1024)
            #The timestamp is given in bytes type
            if time == None:
                print("Connection not working")
            else:
                formatDate(time)
            CSocket.close()
        except KeyboardInterrupt:
            print("\nSIGINT: Connection closed")
    else:
        CSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #Create UDP socket 
        CSocket.sendto("".encode(), (serverName, port))
        time, address = CSocket.recvfrom(1024)
        formatDate(time)
        CSocket.close()


#--------------------------------------------------------------------

def serverMode():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


i = 1
#numerical counter for loop
no = len(sys.argv) - 1
#Number of arguments
serverName = ""
#Name of the server we're going to connect to
mode = "udp"
#Protocol used for the communication
portn = 0
#Number for the selected port (server or client)

for arg in sys.argv[1:]:
    if(arg == "-s" and i < no):
        serverName = sys.argv[i+1]
    elif(arg == "-m" and i < no):
        if(sys.argv[i+1] == "ct"):
            mode ="tcp"
        elif(sys.argv[i+1] == "cu"):
            mode = "udp"
        elif(sys.argv[i+1] == "s"):
            mode = "server"
        else:
            print("Usage is -m [cu] [ct] [s]")
            sys.exit()
    elif(arg == "-p" and i < no):
        try:
            portstr = sys.argv[i+1]
            portnum = int(portstr)
            if(portnum < 0 or portnum > 65535):
                raise Exception("Port number out of bounds")
        except:
            print("Introduce an available port number, 0-65.535")
            sys.exit()
        portn = portnum
    i+=1

if(mode == "server"):
    #serverMode()
    sys.exit()
    
else:
    #TCP or UDP mode
    clientMode(mode, serverName, portn)





