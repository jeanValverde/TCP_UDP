
# UDP y TCP en Python y Go

El tres en l ́ınea, o mejor conocido como gato, el juego que alguna vez todos hemos visto en alg ́un
punto ya sea de la etapa escolar o universitaria, por lo que, se asume que tienen conocimiento de
sus reglas. Es en este contexto donde, para una primera parte, se les encomendar ́a llevar a cabo
la creaci ́on de este juego, en un contexto de Jugador versus Computadora. Para llevar a cabo esta
tarea, se les recomienda revisar el diagrama que se encuentra m ́as abajo.
Como fue mencionado, deber ́an construir una arquitectura cliente-servidor para este juego, el cual,
constar ́a de tres nodos:

* Cliente
* Servidor Intermediario
* Servidor Gato




## Cliente

Este proceso cumple el rol de jugador. El cliente debe satisfacer las siguientes tareas:

* Establecer una conexi ́on TCP con el servidor intermediario.
* No debe conectarse directamente con el Servidor Gato.
* Debe mostrar por consola los resultados de cada uno de los turnos y luego el resultado final, indicando si gan ́o la m ́aquina, el jugador o hubo un empate, para, por ultimo, solicitar una nueva partida o directamente terminar todo.
* El codigo de este programa debe estar escrito en Python.


## Servidor - Intermediario

Este nodo cumple el rol de comunicar el Cliente con el Servidor Gato. Para esto, se deben satisfacer
las siguientes tareas:

* Mantener una conexi ́on TCP con el Cliente.
* Conectarse, cuando sea requerido, con el Servidor Gato mediante una conexi ́on UDP.
* Responder al Cliente con el mensaje que recibe del Servidor Gato.
* Este debe procesar el turno revisando posibles ganadores y enviar el resultado junto con la jugada al Cliente.
* Alertar al Servidor Gato del t ́ermino del juego para que, este pueda terminar su ejecuci ́on
* Debe terminar su ejecuci ́on cuando el Cliente le indique el termino del juego (No sin antes igualmente notificar al Servidor Gato).
* El codigo de este programa debe estar en Python.
* Informar sobre el intercambio de mensajes entre los demas nodos.


## Servidor Gato

Este nodo cumple el rol de BOT en la l ́ogica del Jugador versus Computadora. Por lo tanto,
este nodo juega contra el Cliente ejecutando jugadas aleatorias hasta que se le indique el final del
juego. Para esto, se deben satisfacer las siguientes tareas

* Abrir una conexion UDP para comunicarse con el Servidor Intermediario.
* Abrir otra conexion UDP en un puerto aleatorio (entre 8000 y 65.535) cada vez que se pida una jugada.
* Enviar mensajes al Servidor Intermediario y tambi ́en recibir mensajes del mismo.
* Debe terminar su ejecuci ́on cuando se lo indique el Servidor Intermediario.
* El codigo de este programa debe estar escrito en Go.
* Informar de intercambios de mensajes dentro de su consola, junto con la apertura y cierre de puertos.
