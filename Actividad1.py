import random
import numpy as np

#Engloba la lógica de todo el código
class CleaningRobotSimulation:
    #Se ejecuta cuando se crea una instancia de la clase 
    def __init__(self, M, N, num_agents, dirty_percentage, max_steps):
        #Tamaño de la habitación
        self.M = M  # Numero de filas
        self.N = N  # Numero de columnas 
        self.num_agents = num_agents  # Numero de robots
        self.dirty_percentage = dirty_percentage  # Porcentaje inicial de celdas sucias 
        self.max_steps = max_steps  # Número máximo de pasos en la simulación 
        self.room = self.initialize_room()  # Inicializa el cuarto
        self.agents_positions = [(0, 0)] * num_agents  # Inicializa la posición de todos los robots en (0, 0)
        self.steps_taken = 0 #Pasos tomados durante la simulación
        self.total_moves = 0 #Pasos finales tomados durante la simulación

    #Inicializa la habitación con el porcentaje de celdas suicas    
    def initialize_room(self):
        room = np.zeros((self.M, self.N), dtype=int) #Crea una matriz de ceros 
        num_dirty_cells = int(self.M * self.N * self.dirty_percentage / 100) #Calcula cuántas celdas deben estar sucias
        dirty_cells = random.sample([(i, j) for i in range(self.M) for j in range(self.N)], num_dirty_cells) #Define una lista de celdas aleatorias para ensuciar
        for cell in dirty_cells:
            room[cell] = 1  # 1 representa celda sucia
        return room #retorna la matriz lista para la simulación. 
    
    #Define si todas las celdas están limpias
    def is_clean(self):
        return np.sum(self.room) == 0 #Si la suma de todos los valores de la matriz es 0, la habitaci´øn está limpia
    
    #Elige una posición aleatoria para el agente 
    def move_agent(self, position):
       #Lista de tuplas que almacena las 8 direcciones posibles 
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Arriba, Abajo, Izquierda, Derecha
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
        ]
        while True:
            dx, dy = random.choice(directions) #Elige una dirección al azar
            #Se garantiza que el movimiento nuevo quede dentro de los límites de la matriz
            new_x = max(0, min(self.M - 1, position[0] + dx))
            new_y = max(0, min(self.N - 1, position[1] + dy))
            if (new_x, new_y) != position:  # Garantiza que sea una posición nueva
                return new_x, new_y
    #Corre la simulación y recolecta las estadísticas
    def run_simulation(self): 
        #Garantiza que se mantenga dentro del límite de celdas
        for step in range(self.max_steps):
            if self.is_clean():
                break  #Detiene el ciclo si todo está limpio
            for i in range(self.num_agents):
                #Comportamiento agentes
                x, y = self.agents_positions[i]
                if self.room[x, y] == 1:  # Si la celda está sucia
                    self.room[x, y] = 0  # Limpiar la celda
                else:
                    # Si la celda está limpia, moverse a una celda nueva
                    new_position = self.move_agent((x, y)) 
                    self.agents_positions[i] = new_position #Actualizar posiciones
                    self.total_moves += 1 #Actualizar contador
            self.steps_taken += 1 #Actualizar contador

        # Recolectar resultados
        clean_percentage = 100 * (1 - np.sum(self.room) / (self.M * self.N)) #Calcula el porcentaje limpio
        return {
            "steps_taken": self.steps_taken,
            "clean_percentage": clean_percentage,
            "total_moves": self.total_moves
        }

# Parametros de simulacion
M = 10  # Filas
N = 10  # Columnas
num_agents = 5  # Robots
dirty_percentage = 30  # Porcentaje inicial de celdas sucias
max_steps = 10  # Número máximo de pasos en la simulación

#Correr la simulación
simulation = CleaningRobotSimulation(M, N, num_agents, dirty_percentage, max_steps)
results = simulation.run_simulation()

# Mostrar los resultados
print("Resultados de la simulación:")
print(f"Pasos tomados: {results['steps_taken']}")
print(f"Porcentaje de celdas limpias después de la simulación: {results['clean_percentage']:.2f}%")
print(f"Total de movimientos por los agentes : {results['total_moves']}")
