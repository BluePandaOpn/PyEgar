import pygame
from ...Components.default_logic import move_logic

class CharacterBody2D:
    def __init__(self):
        # 1. Coordenadas de posición (Usamos floats para suavidad con DT)
        self.x = 0.0
        self.y = 0.0
        
        # 2. Configuración de movimiento
        self.speed = 200.0        # Píxeles por segundo
        self._mov_enabled = False
        
        # 3. Bus de datos de estado (Recibe el dt desde Wind.py)
        self._eg_state = {"dt": 0.0}
        
        # 4. Dimensiones para dibujo y colisión (Modo .draw)
        self.ancho = 0
        self.alto = 0
        
        # 5. Variables de dirección (1 = Derecha/Abajo, -1 = Izquierda/Arriba)
        self.x_direction = 0
        self.y_direction = 0

    def eg_Speed(self, speed):
        """Define la velocidad de movimiento (px/s)."""
        self.speed = float(speed)

    def mov(self):
        """Habilita el control por teclado (Flechas/WASD)."""
        self._mov_enabled = True

    def _internal_body_update(self, screen):
        """
        Lógica física interna. 
        Calcula la nueva posición basada en el tiempo real transcurrido.
        """
        if self._mov_enabled:
            # Obtenemos el Delta Time inyectado por el motor
            dt = self._eg_state.get("dt", 0.0)
            
            # Calculamos movimiento usando la lógica central
            # Retorna: (nueva_x, nueva_y, dir_x, dir_y)
            nueva_x, nueva_y, dir_x, dir_y = move_logic(
                self.x, self.y, self.speed, dt
            )
            
            self.x = nueva_x
            self.y = nueva_y
            self.x_direction = dir_x
            self.y_direction = dir_y

        # Sincronización con el componente de dibujo si existe
        if hasattr(self, 'eg_draw'):
            # El dibujo sigue a la entidad
            self.eg_draw.x = self.x
            self.eg_draw.y = self.y