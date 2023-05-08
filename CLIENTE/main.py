from config import *
import socket as socket


"""
@return void
@def inicia un servidor en un puerto especifico y el host en el archivo de configuracion
"""
def openConn(): 
    # Crear un objeto socket para el protocolo TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Vincular el socket a la dirección IP y el puerto
    client_socket.connect((CONFIG['host'],  CONFIG['port']))  
    return client_socket

def connClose(client_socket):
    client_socket.close()


def sendMensage(client_socket, message): 
    client_socket.send(message.encode())


def solicitarPartida(client_socket):
    message = CONFIG['play']
    sendMensage(client_socket, message)
    return True       

def getResponse(client_socket):
    response = client_socket.recv(1024)
    return response.decode()


def main():
    client_socket = openConn()
    solicitarPartida(client_socket)

    message = getResponse(client_socket)
    print("Respuesta del servidor: {}".format(message)) 
 
    connClose(client_socket)


main()
