#!/usr/bin/python3

import sys
import socket
from datetime import datetime
import time as t
import threading 

SETENTA = 2208988800
#Tiempo en segundos equivalente a setenta años

#Funcion que devuelve la IP local del host 
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # ip de prueba, no tiene por qué ser ni accesible
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def formatDate(input):
    timestamp = int.from_bytes(input,"big") 
    #Convierte los bytes del timestamp a int en orden big endian
    ahora = datetime.fromtimestamp((timestamp-SETENTA))
    formatdate = ahora.strftime("%a %b %d %H:%M:%S %Y")
    #Da forma al output de la hora
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




#Funcion que procesa el sistema de hora desde parte del cliente
def clientMode(mode, servername, port = 37):
    if(servername == ""):
        print("Nombre de servidor no especificado, usar con -s")
        sys.exit()
    if(mode == "tcp"):
        try:
            CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #Crea socket TCP
            CSocket.connect((serverName, port))
            #Conecta al servidor y puerto pasados por parametro
            #Usamos el while para que reciba el tiempo del servidor constantemente, funcion pedida en el enunciado
            while True:
                #The default port to get time from a server is 37, specify in program arguments using -p if a different one is wanted
                #print("1")
                time = CSocket.recv(1024)
                #Recibe datos del servidor al que se ha conectado
                if time == None or time == b'':
                    #Si no ha devuelto ninguna hora
                    print("Conexión no funciona o ha sido cerrada")
                    break
                else:
                    #Si el programa ha funcionado sin problema
                    formatDate(time)
        except TimeoutError:
            print("El servidor no da respuesta")
        except KeyboardInterrupt:
            print("\nSIGINT: Connection closed")
        except ConnectionRefusedError:
            print("No se ha podido conectar al servidor")
        CSocket.close()
    else:
        #Si el modo es UDP
        try:
            CSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #Creamos socket UDP
            CSocket.sendto("".encode(), (serverName, port))
            #Enviamos un paquete vacio al servidor para que nos pueda responder con la hora
            time, address = CSocket.recvfrom(1024)
            #Recibimos los datos enviados desde el servidor
            formatDate(time)
            #Damos forma a la hora y tiempo
        except:
            #Si no se recibe respuesta, muestra mensaje alternativo
            print("El servidor al que intenta contactar no responde, compruebe la direccion y puerto introducido")
        CSocket.close()
        


#--------------------------------------------------------------------

#Recoge peticiones TCP
def handle_client_tcp(client_socket):
    try:
        while True:
            timestamp = getDate()
            client_socket.send(timestamp)
            t.sleep(1)
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()
        
def serverMode(portnum):
    try:
        ip = get_local_ip()
        print("Servidor establecido en " + str(ip) + ", en puerto " + str(portnum))
        SSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SSocket.bind((ip, portnum))
        SSocket.listen(5)

        while True:
            try:
                (client_socket, client_address) = SSocket.accept()
                client_handler = threading.Thread(target=handle_client_tcp, args=(client_socket,))
                client_handler.start()
            except KeyboardInterrupt:
                print("SIGINT: closing server")
                SSocket.close()
                sys.exit(0)
    except OSError:
        print("Puerto en uso")
        sys.exit(1)

i = 1
#Contador para el loop
no = len(sys.argv) - 1
#Cuenta el numero de argumentos proporcionados al programa
serverName = ""
#Nombre del servidor al que nos vamos a conectar
mode = "udp"
#Protocolo que usamos para la comunicacion
portn = 0
#Numero de puerto que vamos a usar (server o client)

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
            print("Forma: -m [cu] [ct] [s]")
            sys.exit()
    elif(arg == "-p" and i < no):
        try:
            portstr = sys.argv[i+1]
            portnum = int(portstr)
            if(portnum < 0 or portnum > 65535):
                raise Exception("Numero de puerto fuera de rango")
        except:
            print("Introduzca un numero de puerto válido, 0-65.535")
            sys.exit()
        portn = portnum
    i+=1
if(portn == 0):
    portn = 37
    #Para que puerto 37 sea el default (si no se le da ningun valor)
if(mode == "server"):
    #serverMode()
    serverMode(portn)
    
else:
    #TCP or UDP mode
    clientMode(mode, serverName, portn)





