package main

import (
	"fmt"
	"net"
)

const (
	IP         = "127.0.0.1"
	HOST       = 8484
	PROTOCOLO  = "udp"
	DISPONIBLE = "NO"
)

func main() {

	IPHOST := fmt.Sprintf("%s:%d", IP, HOST)

	fmt.Printf("Servidor GATO conectado como: %s\n", IPHOST)

	// Definir la dirección IP y el puerto del servidor
	serverAddr, err := net.ResolveUDPAddr(PROTOCOLO, IPHOST)
	if err != nil {
		panic(err)
	}

	// Crear un objeto socket para el protocolo UDP
	serverConn, err := net.ListenUDP("udp", serverAddr)
	if err != nil {
		panic(err)
	}
	defer serverConn.Close()

	fmt.Printf("Servidor escuchando en %s\n", serverConn.LocalAddr().String())

	for {
		// Recibir un mensaje del cliente
		buffer := make([]byte, 1024)
		n, clientAddr, err := serverConn.ReadFromUDP(buffer)
		if err != nil {
			panic(err)
		}

		// Imprimir el mensaje recibido
		fmt.Printf("Mensaje recibido de %s: %s\n", clientAddr.String(), buffer[:n])

		// Enviar una respuesta al cliente
		response := []byte("Hola, cliente!")
		_, err = serverConn.WriteToUDP(response, clientAddr)
		if err != nil {
			panic(err)
		}
	}

}
