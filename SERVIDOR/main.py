from config import *
import socket as socket
import uuid
import struct
from cat import Cat
import json
import random

"""

Este nodo cumple el rol de comunicar el Cliente con el Servidor Gato.

Para esto, se deben satisfacer las siguientes tareas:
• Mantener una conexion TCP con el Cliente.
• Conectarse, cuando sea requerido, con el Servidor Gato mediante una conexion UDP.
• Responder al Cliente con el mensaje que recibe del Servidor Gato.
• Este debe procesar el turno revisando posibles ganadores y enviar el resultado junto con la
jugada al Cliente.
• Alertar al Servidor Gato del termino del juego para que, este pueda terminar su ejecucion
• Debe terminar su ejecucion cuando el Cliente le indique el termino del juego (No sin antes
igualmente notificar al Servidor Gato).
• El codigo de este programa debe estar en Python.
• Informar sobre el intercambio de mensajes entre los demas nodos.

"""



"""
@return void
@def inicia un servidor en un puerto especifico y el host en el archivo de configuracion
"""
def openConn(): 
    # Crear un objeto socket para el protocolo TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Vincular el socket a la dirección IP y el puerto
    server_socket.bind((CONFIG['host'],  CONFIG['port'])) 
    # Escuchar las conexiones entrantes
    server_socket.listen(1) 
    print("Servidor escuchando en {}:{}".format(CONFIG['host'],  CONFIG['port']))
    return server_socket

 
"""
@return void
@def cierra la conexion 
"""
def closeConn(server_socket):
    server_socket.close()


"""
@return void
@def cierra la conexion 
"""
def listen(server_socket):
    client_socket, client_address = server_socket.accept()
    return client_socket, client_address

def sendRequestBOT(request):
    return "OK"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CONFIG['host'], 8484)) 
        print("Enviando mensaje a BOT: {}".format(request))
        s.sendall(request)
        response = s.recv(1024) 
        return response.decode()
        
def format_server_encode(message:str, cat:Cat):
    datos = {
        'message': message,
        'cuerpo': '',
        'cat': {
            'id':cat.id,
            'tablero':cat.cuadricula, 
            'juego':{
                'x':'', 
                'y':''
            }, 
            'posibles':cat.posibles, 
            'terminado':cat.terminado, 
            'name_ganador':cat.name_ganador,
            'ganador':cat.ganador()
        }
    }
    return json.dumps(datos) 

def format_server_encode_only(message:str):
    datos = {
        'message': message,
        'cuerpo': '',
        'cat': {
            'id':'',
            'tablero':[], 
            'juego':{
                'x':'', 
                'y':''
            }, 
            'posibles':[], 
            'terminado': True
        }
    }
    return json.dumps(datos) 

def format_server_decode(response):
    return json.loads(response)



def send_message_bot(message:str, cat:Cat):
    try:
        # Crea un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Envía un mensaje UDP al servidor en la dirección y puerto especificados
        server_address = ('localhost', 1)  # Utiliza cualquier puerto disponible 
        
        #parsear cat
        cat_json = format_server_encode(message, cat)
        
        sock.sendto(cat_json.encode(), server_address)

        # Espera la respuesta del servidor
        data, server = sock.recvfrom(1024)
        # Cierra el socket
        sock.close()
        
        print('Mensaje recibido desde', server, ':', data.decode()) 
        data = format_server_decode(data.decode())   
        
        return data['message'], data['cat'] 
    
    except Exception as e:  
        print('Error al conectarse con BOT')
    
    
def get_jugada_bot(cat_cliente):
    
    message_out , cat_bot = send_message_bot("JUGANDO",  cat_cliente ) 
    
    x = cat_bot["juego"]["x"]
    y = cat_bot["juego"]["y"]
    
    return x,y
    
    #pasar este codigo a GO 
    
    #valor = random.randint(0, 8)   
    #dos casos no hay mas juagadas 
    #existe juagda
    #if posibles[valor] is not None:
    #    data = posibles[valor].split(',')
    #    return data[0], data[1]
    
    #sin_jugadas = False
    #for posible in range(0, 9):
    #    if posibles[posible] is not None:
    #        sin_jugadas = True
    
    #if sin_jugadas:
    #    return get_jugada_bot(posibles)
    
    #return 10,10
    


#Puede recibir del cliente 
#jugada
#mensaje
def get_menssage_cliente(client_socket):
    # Recibir los datos
    data = client_socket.recv(1024) 
    data = format_server_decode(data.decode())   
    return data['message'], data['cat']

#Puedo enviar a cliente 
#mensaje 
#esado de juego
def send_message_cliente_by_cat(client_socket, message, cat): 
    #send
    request = format_server_encode(message, cat)
    client_socket.send(request.encode())
    #print("Enviado respuesta a cliente: ", request)
    return "mensaje enviado"

def send_message_cliente_only(client_socket, message):
    #send
    request = format_server_encode_only(message)
    client_socket.send(request.encode())
    return "mensaje enviado"


def isSolicitudJuego(client_socket,):
    message, cat_cliente = get_menssage_cliente(client_socket)  
   
    if message == CONFIG['play']: 
        numero = random.randint(1, 9999)
        cat_nuevo = Cat("CAT-CLI-"+str(numero)) 
    
        #llamar a BOT para ver si es posbible jugar   
        message, cat = send_message_bot(message, cat_nuevo)
        
        #segun BOT 
        if message == "OK": 
            #responder a cliete y crear la partida 
            send_message_cliente_by_cat(client_socket, message ,cat_nuevo )
            return (True , message, cat_nuevo , cat_cliente)
        
    return (False , message, None, cat_cliente) 



def update_cat(id, cats, x, y, jugador):
    for cat in cats: 
        if cat.id == id:
            cat.update(int(x), int(y), jugador)  
            return cat
    return None


cats = []

def main(): 
    
    
    try:
        server_socket = openConn() 
        if server_socket is None:
            raise TypeError("Error desconocido en el servidor")
        
        while True:
            # Aceptar conexiones entrantes
            client_socket, client_address = listen(server_socket)
            
            isNuevo, disponible, cat_nuevo, cat_cliente = isSolicitudJuego(client_socket) 
            
            #agregamos un nuevo juego para el cliente X 
            if cat_nuevo is not None:
                cats.append(cat_nuevo)
            
            if not isNuevo:
                #Estamos jugando o es un NO 
                if disponible == 'NO':
                    send_message_cliente_only(client_socket, disponible)
                else:
                    #marcar la jugada del cliente  y verificar quien es el ganador  
                    cat_cliente = update_cat(cat_cliente["id"], cats, cat_cliente['juego']['x'], cat_cliente['juego']['y'] , "cliente")
                    
                    if cat_cliente.is_terminado() is False:
                        #soliciar juagada a BOT 
                        #x,y = get_jugada_bot(cat_cliente.get_posibles_lineal())
                        
                        x,y = get_jugada_bot(cat_cliente)
                        
                        #message_out , cat_bot = send_message_bot("JUGANDO",  cat_cliente ) 
                        print("JUEGO DIRECTO DESDE BOT ", x , y)
                        
                        #terminar partida, verificar quien gana, enviar el ganador 
                        if x != 10 and y != 10: 
                            cat_cliente = update_cat(cat_cliente.id, cats, x, y , "BOT")
                         
                    send_message_cliente_by_cat(client_socket, disponible, cat_cliente) 
                
                
            # Cerrar la conexión con el cliente
            client_socket.close()

    except Exception as e:
        print("Error en el servidor: " + str(e))

main()

