class GuiGato: 

    def __init__(self):
        print("- - - - - - - - Bienvenido al Juego - - - - - - - -")

    def start(self):
        print("- Seleccione una opcion")
        print("1-Jugar")
        print("2-Salir")
        opt = self.get_opcion() 
        return opt
        
    def get_opcion(self):
        opt = input('')
        try:
            opt = int (opt)
            return opt
        except Exception as e:    
            print("Debe ser un numero")
            opt = self.get_opcion()
            
    def isPartida(self,responseServidor):
        print("respuesta de disponibilidad: {}", responseServidor )
        if responseServidor == 'OK':
            return True
        return False
    
    def pintar_cuadricula(self,cuadricula): 
        for fila in cuadricula: 
            print(fila[0] or ' ', '|', fila[1] or ' ', '|', fila[2] or ' ')
            print('--+---+--')
            
    def get_jugada(self): 
        entrada = input('Ingrese su jugada (x,y):')
        jugada = entrada.split(',')
        return jugada[0], jugada[1]
    
        