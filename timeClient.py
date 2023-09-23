#!/usr/bin/python3

import sys
import socket
from datetime import datetime
import time as t

SETENTA = 2208988800
#Represents the time in seconds equivalent to seventy years time


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def formatDate(input):
    timestamp = int.from_bytes(input,"big") 
    #Converts the bytes pseudotimestamp into an integer using big endian order
    ahora = datetime.fromtimestamp((timestamp-SETENTA))
    formatdate = ahora.strftime("%a %b %d %H:%M:%S %Y")
    print(formatdate)

def getDate():
    ahora = datetime.timestamp(datetime.now())
    #Turns actual time into timestamp
    ahora = int(ahora) + SETENTA
    #Converts float into int to be able to cast to bytes
    date = ahora.to_bytes(5, "big")
    #Converts ahora into a 5 pos long bytes array big endian
    return date 


#-------------------------------------------------------------------

def clientMode(mode, servername, port = 37):
    if(servername == ""):
        print("Server name not specified, set using -s")
        sys.exit()
    if(mode == "tcp"):
        try:
            CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CSocket.connect((serverName, port))
            while True:
                #The default port to get time from a server is 37, specify in program arguments using -p if a different one is wanted
                #print("1")
                time = CSocket.recv(1024)
                #The timestamp is given in bytes type
                if time == None or time == 0:
                    print("Connection not working")
                    break
                else:
                    formatDate(time)
                
        except KeyboardInterrupt:
            print("\nSIGINT: Connection closed")
        except ConnectionRefusedError:
            print("No se ha podido conectar al servidor")
        CSocket.close()
    else:
        try:
            CSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #Create UDP socket 
            CSocket.sendto("".encode(), (serverName, port))
            time, address = CSocket.recvfrom(1024)
            formatDate(time)
        except:
            print("El servidor al que intenta contactar no responde, compruebe la direccion y puerto introducido")
        CSocket.close()
        


#--------------------------------------------------------------------

def serverMode(portnum):
    ip = get_local_ip()
    print("Servidor establecido en " + str(ip) + ", en puerto " + str(portnum))
    SSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SSocket.bind((ip, portnum))
    #Bind server ip address to port
    SSocket.listen(5)
    (clientx, clientAddr) = SSocket.accept()
    while True:
        try:
            timestamp = getDate()
            print("1")
            clientx.send(getDate())
            t.sleep(1)
        except KeyboardInterrupt:
            print("SIGINT: closing server")
            SSocket.close()
            sys.exit(0)


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
    serverMode(portn)
    
else:
    #TCP or UDP mode
    clientMode(mode, serverName, portn)





