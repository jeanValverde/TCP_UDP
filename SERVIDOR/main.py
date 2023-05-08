from config import *
import socket as socket
 
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
        

def jugar(client_socket, client_address): 
    return True


def sendRequestBOT(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CONFIG['host'], 8484)) 
        print("Enviando mensaje a BOT: {}".format(request))
        s.sendall(request)
        response = s.recv(1024) 
        return response.decode()


def main():
    try:
        server_socket = openConn() 
        if server_socket is None:
            raise TypeError("Error desconocido en el servidor")

        #jugar(client_socket, client_address)

        while True:
            # Aceptar conexiones entrantes
            client_socket, client_address = listen(server_socket)

            #print("Conexión entrante de {}:{}".format(client_address[0], client_address[1]))

            # Recibir datos del cliente
            data = client_socket.recv(1024)

            # Imprimir los datos recibidos
            print("Mensaje recibido: {}".format(data.decode()))

            response = sendRequestBOT(data.decode())
            
            #if response == "NO":
            print("Mensaje recibido desde BOT e intermediario SERVIDOR: {}".format(response))
              
            # Enviar una respuesta al cliente
            response = "Hola, cliente!"
            client_socket.send(response.encode())

            # Cerrar la conexión con el cliente
            client_socket.close()

    except Exception as e:
        print("Error en el servidor: " + str(e))

main()

