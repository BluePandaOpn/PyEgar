import pygame
import math

class Gravity2D:
    def __init__(self):
        # Propiedades Físicas Base
        self.gravity = 0.6
        self.jump_force = -14.0
        self.friction = 0.1         # Coeficiente de fricción horizontal
        self.mass = 1.0             # Masa del objeto para cálculos de fuerza
        
        # Vectores de Estado
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.terminal_velocity = 16.0
        
        # Estados de Control
        self.is_on_floor = False
        self._gravity_enabled = False

    def eg_Gravity(self, gravity=0.6, jump=-14.0):
        """Define la aceleración gravitatoria y potencia de salto."""
        self.gravity = gravity
        self.jump_force = jump
        self._gravity_enabled = True

    def eg_Friction(self, value=0.1):
        """Define el coeficiente de fricción (0.0 a 1.0) para el frenado automático."""
        self.friction = value

    def eg_Force(self, fx=0.0, fy=0.0):
        """Aplica un impulso instantáneo al objeto (Segunda Ley de Newton: F=m*a)."""
        self.velocity_x += fx / self.mass
        self.velocity_y += fy / self.mass

    def _apply_gravity(self, entity):
        """Procesa el motor de físicas integral (Gravedad + Fricción + Movimiento)."""
        if not self._gravity_enabled:
            return

        # 1. Gestión de Salto
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_on_floor:
            self.velocity_y = self.jump_force
            self.is_on_floor = False

        # 2. Aplicar Gravedad (Eje Y)
        if not self.is_on_floor:
            self.velocity_y += self.gravity
            if self.velocity_y > self.terminal_velocity:
                self.velocity_y = self.terminal_velocity

        # 3. Aplicar Fricción (Eje X) - Frenado Progresivo
        # Si no se pulsan teclas de movimiento, la fricción detiene al objeto
        if abs(self.velocity_x) > 0.1:
            self.velocity_x *= (1.0 - self.friction)
        else:
            self.velocity_x = 0

        # 4. Actualización de posición final
        entity.y += self.velocity_y
        entity.x += self.velocity_x