package main

import (
	"fmt"
	"net"
    "encoding/json"
    "math/rand"
    "time"
    "strings"
    "reflect"
)

type Juego struct {
    Message string `json:"message"`
    Cuerpo string `json:"cuerpo"`
    Cat struct {
        ID string `json:"id"`
        Tablero [][]interface{} `json:"tablero"`
        Juego struct {
            X string `json:"x"`
            Y string `json:"y"`
        } `json:"juego"`
        Posibles [][]interface{} `json:"posibles"`
        Terminado bool `json:"terminado"`
        NameGanador interface{} `json:"name_ganador"`
        Ganador interface{} `json:"ganador"`
    } `json:"cat"`
}

func removeNil(arr [][]interface{}) [][]string {
	var result [][]string

	for _, innerArr := range arr {
		var newInnerArr []string
		for _, val := range innerArr {
			if val == nil {
				newInnerArr = append(newInnerArr, "-")
			} else {
				newInnerArr = append(newInnerArr, reflect.ValueOf(val).String())
			}
		}
		result = append(result, newInnerArr)
	}

	return result
}

func createLinearArray(arr [][]string) []string {
    linearArr := []string{}
    for _, row := range arr {
        for _, elem := range row {
            linearArr = append(linearArr, elem)
        }
    }
    return linearArr
}

func get_jugada_bot(posibles []string) (string, string) {
    
    rand.Seed(time.Now().UnixNano()) // inicializar la semilla del generador de números aleatorios
    
    valor := rand.Intn(9) // generar un número aleatorio entre 0 y 8
    // dos casos: no hay más jugadas, existe jugada
    if posibles[valor] != "-" {
        data := strings.Split(posibles[valor], ",")
        return data[0], data[1]
    }

    sinJugadas := false
    for _, posible := range posibles {
        if posible != "-" {
            sinJugadas = true
            break
        }
    }
    
    if sinJugadas {
        return get_jugada_bot(posibles)
    }
    
    return "10", "10"
}

func get_cat(jsonStr string) (Juego, error) { 
    var juego Juego
    err := json.Unmarshal([]byte(jsonStr), &juego)
    if err != nil {
        panic(err)
    }
    return juego, err
}


func main() {
	// Crea una dirección UDP genérica para recibir mensajes en cualquier puerto
	addr, err := net.ResolveUDPAddr("udp", ":1")
	if err != nil {
		fmt.Println("Error al resolver la dirección UDP:", err)
		return
	}

	// Crea un socket UDP para recibir mensajes en la dirección especificada
	sock, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println("Error al abrir el socket UDP:", err)
		return
	}
	defer sock.Close()

	// Bucle infinito para recibir mensajes y responder
	buf := make([]byte, 1024)
	for {
		n, addr, err := sock.ReadFromUDP(buf)
		if err != nil {
			fmt.Println("Error al recibir el mensaje UDP:", err)
			continue
		}

		// Imprime el mensaje recibido
        
		fmt.Println("Mensaje recibido desde", addr.String(), ":", string(buf[:n]))
      
        Juego, err := get_cat(string(buf[:n])) 
        if err != nil {
            fmt.Println("Error al parsear el JSON:", err)
            return
        }
        fmt.Println("ID del Cat:", Juego.Cat.ID)
        
        if (Juego.Message == "JUGANDO"){
            //posible partida  
            var posibles = removeNil(Juego.Cat.Posibles)
            fmt.Println(createLinearArray(posibles))

            x, y := get_jugada_bot(createLinearArray(posibles))
            Juego.Cat.Juego.X = x
            Juego.Cat.Juego.Y = y
        }

        if ( Juego.Message == "SOLICITUD_JUEGO" ) {
            Juego.Message = "OK"
        }
 
        // Pasar la estructura a string
	    catStr, _ := json.Marshal(Juego)

		// Responde con un mensaje de confirmación
		reply := []byte("" +  string(catStr) )
		_, err = sock.WriteToUDP(reply, addr)
		if err != nil {
			fmt.Println("Error al enviar el mensaje de confirmación:", err)
			continue
		}
      

		// Imprime el mensaje de confirmación enviado
		fmt.Println("Mensaje de confirmación enviado a", addr.String() , ": data : " ,  string(catStr))
	}
}
