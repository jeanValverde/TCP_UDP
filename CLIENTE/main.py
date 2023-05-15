from config import *
import socket as socket
import json
from gui import GuiGato
import struct


"""

Este proceso cumple el rol de jugador. 

El cliente debe satisfacer las siguientes tareas:

• Establecer una conexion TCP con el servidor intermediario.
• No debe conectarse directamente con el Servidor Gato.
• Debe mostrar por consola los resultados de cada uno de los turnos y luego el resultado final,
indicando si gana la maquina, el jugador o hubo un empate, para, por ultimo, solicitar una
nueva partida o directamente terminar todo.
• El codigo de este programa debe estar escrito en Python.


"""


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

def closeConn(client_socket):
    client_socket.close()

def format_server_encode(message:str, body:str, id, x, y):
    datos = {
        'message': message,
        'cuerpo': body,
        'cat': {
            'id':id,
            'tablero':[], 
            'juego':{
                'x': x, 
                'y': y
            }, 
            'posibles':[], 
            'terminado':False,
            'name_ganador':'',
            'ganador':''
        }
    }
    return json.dumps(datos) 

def format_server_decode(response):
    return json.loads(response)


def sendMensage(client_socket, message, cuerpo, id, x, y ): 
    # Serializar los datos y enviarlos 
    # Enviar un mensaje al servidor 
    request = format_server_encode(message, cuerpo, id, x, y ) 
    client_socket.send(request.encode()) 
    
    # Recibir los datos
    response = client_socket.recv(1024) 
    data = format_server_decode(response.decode()) 
    return (data["message"], data["cat"])


def solicitarPartida():  
    client_socket = openConn()
    return sendMensage(client_socket, CONFIG['play'] , '', '', '', '' )   


def getEstadoJuego(idCat): 
    client_socket = openConn()
    message, data = sendMensage(client_socket, idCat, '')
    return data

def send_jugada(id, x, y):
    client_socket = openConn()
    message, cat = sendMensage(client_socket, "JUGANDO", "", id , x, y) 
    return cat
    

def main(): 
    
    gui = GuiGato() 
    opt = gui.start()
    
    if opt == 1:
        message, cat = solicitarPartida() 
         
        is_partida_nueva = gui.isPartida(message)
        
        if is_partida_nueva:
            #iniciar el juego hasta que termine 
            terminado = cat['terminado']
            while terminado == False:
                gui.pintar_cuadricula(cat['tablero'])
                x, y = gui.get_jugada()
                #con la jugada enviar a servidor para atualizar estados
                cat = send_jugada(cat['id'], x, y)
                
                #verificar quien gano
                terminado = cat['terminado']
                if terminado:
                    gui.pintar_cuadricula(cat['tablero'])
                    print(cat['ganador'])  
    else:
        print("Bye")
        
main()


