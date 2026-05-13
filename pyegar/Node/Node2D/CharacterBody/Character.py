import pygame
from ....Components.Default.default_logic import move_logic

class CharacterBody2D:
    def __init__(self):
        # 1. Coordenadas de posición (Flotantes para precisión con Delta Time)
        self.x = 0.0
        self.y = 0.0
        
        # 2. Configuración de movimiento
        # Al usar Delta Time, la velocidad se mide en píxeles por segundo (ej. 200)
        self.speed = 100.0
        self._mov_enabled = False
        
        # 3. Bus de datos interno
        # Este diccionario recibe el "dt" automáticamente desde Wind.py
        self._eg_state = {"dt": 0.0}
        
        # 4. Variables de dirección (Para animaciones y Sprites)
        # 1 = Derecha/Abajo, -1 = Izquierda/Arriba, 0 = Quieto
        self.x_direction = 0
        self.y_direction = 0

    def eg_Speed(self, speed):
        """Define la velocidad de movimiento del cuerpo en px/s."""
        self.speed = float(speed)

    def mov(self):
        """Activa el sistema de movimiento por teclado (Flechas/WASD)."""
        self._mov_enabled = True

    def _internal_body_update(self, screen):
        """
        Actualiza la lógica física del cuerpo. 
        Este método es llamado automáticamente por el motor.
        """
        if self._mov_enabled:
            # Extraemos el Delta Time actual del bus de estado
            dt = self._eg_state.get("dt", 0.0)
            
            # Llamamos a move_logic con los 4 parámetros requeridos
            # Retorna: nueva_x, nueva_y, dir_x, dir_y
            self.x, self.y, self.x_direction, self.y_direction = move_logic(
                self.x, self.y, self.speed, dt
            )

    def set_position(self, x, y):
        """Método manual para teletransportar al personaje."""
        self.x = float(x)
        self.y = float(y)

    def get_position(self):
        """Devuelve una tupla con la posición actual."""
        return (self.x, self.y)