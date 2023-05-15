class Cat:
    def __init__(self, id):
        self.id = id
        self.cuadricula = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.posibles = [
            ['0,0', '0,1', '0,2'], 
            ['1,0', '1,1', '1,2'],  
            ['2,0', '2,1', '2,2']  
        ]
        self.next = "cliente"
        self.terminado = False
        self.name_ganador = None
        self.partidas = 0
        
    
    def print(self):
        cat = ""
        for fila in self.cuadricula:
            cat = cat + fila[0] or ' ' + '|' + fila[1] or ' ' + '|' +  fila[2] or ' ' + '\n--+---+--\n'
        return cat
    
    def get_posibles_lineal(self):
        # Crear un solo arreglo
        linea = []
        for fila in self.posibles:
            linea.extend(fila)
        return linea
    
    def tick_posibles(self):
        posibles = " "
        for fila in self.posibles:
            if fila[0] is not None:
                posibles = posibles + " " + fila[0]
            if fila[1] is not None: 
                posibles = posibles + " " + fila[1]
            if fila[2] is not None: 
                posibles = posibles + " " + fila[2]
        return posibles
    
    def update(self, x, y, jugador):
        if jugador == "cliente":
            self.tick_cliente(x,y) 
            return True
        
        if jugador == "BOT":
            self.tick_bot(x,y)
            return True
    
        return False
    
    def tick_cliente(self,x,y):
        if self.next == "cliente":
            self.cuadricula[x][y] = 'X'
            self.posibles[x][y] = None
            self.next = "BOT"
            self.partidas = self.partidas + 1
            self.ganador() 
            return "Siguiente turno para: " + self.next
        else:
            "No es tu turno"
    
    def tick_bot(self,x,y):
        if self.next == "BOT":
            self.cuadricula[x][y] = 'O'
            self.posibles[x][y] = None
            self.next = "cliente"
            self.partidas = self.partidas + 1
            self.ganador() 
            return "Siguiente turno para: " + self.next
        else:
            "No es tu turno"
            
    def is_terminado(self): 
        for fila in self.cuadricula:
            if fila[0] is None:
               return False
            if fila[1] is None: 
                return False
            if fila[2] is None: 
                return False 
        return True


    def ganador(self):
        gana = self.verificar_ganador()
        
        if gana is None: 
            #puede que sea empate and verificar vacio all
            if self.partidas == 9 :
                self.terminado = True
                self.name_ganador = "Empate"
                return "Nadie gana, es un empate"
            
            return None
        
        if gana is not None:
            if gana == "X":
                self.terminado = True
                self.name_ganador = "Cliente"
                return "Ganador es el cliente"
            if gana == "O":
                self.terminado = True
                self.name_ganador = "BOT"
                return "Ganador es el BOT" 
            
    def verificar_ganador(self):
        # Verificar filas
        for fila in self.cuadricula:
            if fila[0] == fila[1] == fila[2] and fila[0] is not None:
                return fila[0]
        
        # Verificar columnas
        for i in range(3):
            if self.cuadricula[0][i] == self.cuadricula[1][i] == self.cuadricula[2][i] and self.cuadricula[0][i] is not None:
                return self.cuadricula[0][i]
        
        # Verificar diagonales
        if self.cuadricula[0][0] == self.cuadricula[1][1] == self.cuadricula[2][2] and self.cuadricula[0][0] is not None:
            return self.cuadricula[0][0]
        if self.cuadricula[0][2] == self.cuadricula[1][1] == self.cuadricula[2][0] and self.cuadricula[0][2] is not None:
            return self.cuadricula[0][2]
        
        # Si nadie ha ganado, devolver None
        return None
    
        
    
