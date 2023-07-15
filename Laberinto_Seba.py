# Laberinto de Sebi Arias B)
from PIL import Image
import math

class Nodo():
    def __init__(self, estado, padre):
        self.estado = estado
        self.padre = padre

    def __str__(self):
        return str(self.estado)

    def n_recorrido(self):
        pass

class Frontera():
    def __init__(self):
        self.frontera = []

    def __str__(self):
        return "Nodos en la frontera: " + " ".join(
            str(nodo.estado) for nodo in self.frontera)

    def agregar_nodo(self, nodo):
        self.frontera.append(nodo)

    def quitar_nodo(self):
        pass

    def esta_vacia(self):
        return len(self.frontera)==0

    def check_estado(self, estado):
        for nodo in self.frontera:
            if nodo.estado == estado:
                return True
        return False

class FronteraStack(Frontera):
    
    def quitar_nodo(self):
        return self.frontera.pop()

class FronteraQeue(Frontera):
    
    def quitar_nodo(self):
        return self.frontera.pop(0)
    
class FronteraGBFS(Frontera):

    def __init__(self, meta):
        super().__init__()
        self.meta = meta

    def __str__(self):
        return "Nodos en la frontera: " + " ".join(
            str(nodo.estado) for nodo,euristica in self.frontera)

    def heuristica(self, estado):
        meta_fila, meta_columna = self.meta
        fila, columna = estado
        return math.sqrt((meta_fila - fila) ** 2 + (meta_columna - columna) ** 2)

    def agregar_nodo(self, nodo):
        heuristica = self.heuristica(nodo.estado)
        self.frontera.append((nodo, heuristica))
        self.frontera.sort(key=lambda x: x[1])  # Ordenar por heurística
    
    def quitar_nodo(self):
        return self.frontera.pop(0)[0]  # Devolver solo el nodo
    
    def check_estado(self, estado):
        for nodo,euristica in self.frontera:
            if nodo.estado == estado:
                return True
        return False

class FronteraAStar(Frontera):

    def __init__(self, meta):
        super().__init__()
        self.meta = meta

    def __str__(self):
        return "Nodos en la frontera: " + " ".join(
            str(nodo.estado) for nodo,costo in self.frontera)

    def costo_fila(self, nodo):
        # Implementa el cálculo del costo g del nodo (costo acumulado desde el nodo inicial hasta el nodo actual)
        meta_fila = self.meta[0]
        fila = nodo.estado[0]
        costo_fila = meta_fila + fila
        return costo_fila

    def costo_col(self, nodo):
        # Implementa el cálculo del costo h del nodo (heurística desde el nodo actual hasta la meta)
        meta_col = self.meta[1]
        col = nodo.estado[1]
        costo_col = meta_col + col
        return costo_col

    def agregar_nodo(self, nodo):
        costo_fila = self.costo_fila(nodo)
        costo_col = self.costo_col(nodo)
        costo_manhattan = costo_fila + costo_col
        self.frontera.append((nodo, costo_manhattan))
        self.frontera.sort(key=lambda x: x[1])  # Ordenar por costo total f = g + h

    def quitar_nodo(self):
        return self.frontera.pop(0)[0]  # Devolver solo el nodo
    
    def check_estado(self, estado):
        for nodo,euristica in self.frontera:
            if nodo.estado == estado:
                return True
        return False

class Laberinto():
    def __init__(self,algoritmo):
        
        with open("Laberinto.txt","r") as archivo:
            laberinto = archivo.read()

        laberinto = laberinto.splitlines()
        self.map_lab = [list(line) for line in laberinto]

        self.ancho = len(laberinto[0])
        self.alto = len(laberinto)
        self.paredes = []
        for fila in range(self.alto):
            paredes_en_fila = []
            for col in range(self.ancho):
                if laberinto[fila][col] == ' ':
                    paredes_en_fila.append(False)
                elif laberinto[fila][col] == 'I':
                    self.inicio = (fila,col)
                    paredes_en_fila.append(False)
                elif laberinto[fila][col] == 'M':
                    self.meta = (fila,col)
                    paredes_en_fila.append(False)
                else:
                    paredes_en_fila.append(True)
            self.paredes.append(paredes_en_fila)
        
        self.solucion = None
        self.algoritmo = algoritmo

    def expandir_nodo(self, nodo):
        fila,columna = nodo.estado      # Guarda el nodo nodo_actual
        vecinos_posibles = []          
        vecinos_confirmados = []
        
        vecinos_posibles = [(fila-1,columna),
                            (fila,columna+1),
                            (fila+1,columna),
                            (fila,columna-1)]

        for f,c in vecinos_posibles:
            
            if 0 <= f < self.alto and 0 <= c < self.ancho and not self.paredes[f][c]:
                vecinos_confirmados.append((f,c))
            else:
                pass
        return vecinos_confirmados
    
    def print_laberinto_inicial(self):
        # tamaño de cada cuadro en píxeles
        cuadrado = 50

        alto = self.alto * cuadrado
        ancho = self.ancho * cuadrado
        # Crea una nueva imagen en blanco con el tamaño calculado
        imagen = Image.new("RGB", (ancho,alto))

        # Itera sobre el laberinto y asigna un color a cada cuadro
        for fila, row in enumerate(self.map_lab):
            for columna, caracter in enumerate(row):
                # Calcula las coordenadas del cuadro en la imagen
                x_inicio = columna * cuadrado
                y_inicio = fila * cuadrado
                x_fin = x_inicio + cuadrado
                y_fin = y_inicio + cuadrado

                # Asigna un color según el caracter del laberinto
                if caracter == '#':
                    color = (0, 0, 0)  # Negro para las paredes
                elif caracter == ' ':
                    color = (255, 255, 255)  # Blanco para los espacios vacíos
                elif caracter == 'I':
                    color = (255, 0, 0)  #ROJO
                elif caracter == 'M':
                    color = (0, 255, 0)  #VERDE

                # Pinta el cuadro en la imagen
                for y in range(y_inicio, y_fin):
                    for x in range(x_inicio, x_fin):
                        imagen.putpixel((x, y), color)

        # Guarda la imagen en formato PNG
        imagen.save('laberinto_init.png')

    def print_laberinto_final(self):
        # tamaño de cada cuadro en píxeles
        cuadrado = 50

        alto = self.alto * cuadrado
        ancho = self.ancho * cuadrado
        # Crea una nueva imagen en blanco con el tamaño calculado
        imagen = Image.new("RGB", (ancho,alto))

        # Itera sobre el laberinto y asigna un color a cada cuadro
        for fila, row in enumerate(self.map_lab):
            for columna, caracter in enumerate(row):
                # Calcula las coordenadas del cuadro en la imagen
                x_inicio = columna * cuadrado
                y_inicio = fila * cuadrado
                x_fin = x_inicio + cuadrado
                y_fin = y_inicio + cuadrado

                # Asigna un color según el caracter del laberinto
                if caracter == '#':
                    color = (0, 0, 0)  # Negro para las paredes
                elif caracter == ' ':
                    color = (255, 255, 255)  # Blanco para los espacios vacíos
                elif caracter == 'I':
                    color = (255, 0, 0)  #ROJO
                elif caracter == 'M':
                    color = (0, 255, 0)  #VERDE
                elif caracter == 'O':
                    color = (236, 212, 97)  #ALBA
                elif caracter == 'X':
                    color = (250, 153, 0)  #NARANJA

                # Pinta el cuadro en la imagen
                for y in range(y_inicio, y_fin):
                    for x in range(x_inicio, x_fin):
                        imagen.putpixel((x, y), color)

        # Guarda la imagen en formato PNG
        imagen.save(f'laberinto_final.png')

    def resolver(self):

        if self.algoritmo=='BFS':
            frontera = FronteraQeue()
        elif self.algoritmo=='DFS':
            frontera = FronteraStack()
        elif self.algoritmo == 'GBFS':
            frontera = FronteraGBFS(self.meta)
        elif self.algoritmo == 'A*':
            frontera = FronteraAStar(self.meta)
            
    #-----------------------------------------------
        nodo_inicial = Nodo(self.inicio, None)
        frontera.agregar_nodo(nodo_inicial)
        self.estados_explorados = []
        self.n_nodos_explorados = 0
        
        while True:

            #Muestro los elementos en frontera
            print(frontera)

            #Compruebo si esta vacia y no hay solucion
            if frontera.esta_vacia():
                print("el laberinto no tiene solucion")
                raise Exception("No hay solucion")
            
            #Quito el nodo actual de la frontera y lo guardo
            nodo_actual = frontera.quitar_nodo()

            # Agrego esta condicion para no re-mapear el self.inicio = 'I'
            if(nodo_actual.padre != None):
                #Remplazo el caracter del nodo quitado por una 'O'
                #Para mapear el recorrido hecho
                self.map_lab[nodo_actual.estado[0]][nodo_actual.estado[1]] = "O"

            #Compruebo si ya llegue a la meta 
            if nodo_actual.estado == self.meta:

                #Asigno 'M' al mapa para cuando se pinte
                self.map_lab[self.meta[0]][self.meta[1]] = "M"

                #Muestro los nodos explorados y el anuncio de meta encontrada
                print(f"nodos explorados: {self.n_nodos_explorados}")
                print("LLEGASTEEEEEEEEEE AHAHAAHAHAAHAHA")

                # Hago la lista y el bucle para rescatar a todos los nodos padres
                self.solucion = []
                while nodo_actual.padre != None:
                    self.solucion.append(nodo_actual.padre)
                    nodo_actual = nodo_actual.padre

                    # Asigno 'X' a todos los nodos padres del mapa
                    self.map_lab[nodo_actual.estado[0]][nodo_actual.estado[1]] = 'X'
                    
                    # Agrego esta condicion para no re-mapear el self.inicio = 'I'
                    if(nodo_actual.padre != None):
                        #Pinto el camino desde meta a inicio
                        self.print_laberinto_final()
                    
                    self.solucion.reverse()
                return self.solucion
            
            self.estados_explorados.append(nodo_actual.estado)
            self.n_nodos_explorados += 1
            estados_confirmados = self.expandir_nodo(nodo_actual)

            for tupla in estados_confirmados:
                if not frontera.check_estado(tupla) and not tupla in self.estados_explorados:
                    nodo = Nodo(tupla,nodo_actual)
                    frontera.agregar_nodo(nodo)
                    self.print_laberinto_final()