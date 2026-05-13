# pyegar/Components/Physics/Gravity.py
import pygame

class Gravity2D:
    def __init__(self):
        # Configuración física
        self.gravity_force = 0.0
        self.jump_force = 0.0
        self.velocity_y = 0.0
        
        # Estados
        self.is_on_floor = False
        self.gravity_enabled = True

    def eg_Gravity(self, force, jump):
        """
        Define la fuerza de gravedad y la potencia de salto.
        Ejemplo: entity.eg_Gravity(0.8, jump=-15)
        """
        self.gravity_force = force
        self.jump_force = jump

    def _apply_gravity(self, entity):
        """
        Calcula la caída y el salto usando Delta Time.
        Inyectado automáticamente por el motor.
        """
        if not self.gravity_enabled:
            return

        # 1. Obtener Delta Time desde el estado del nodo
        dt = getattr(entity, '_eg_state', {}).get("dt", 0.016)
        
        # Multiplicador de escala para que los valores de gravedad 
        # se sientan naturales (ajuste de frames a segundos)
        fps_factor = 60.0 

        # 2. LÓGICA DE SALTO
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_on_floor:
            self.velocity_y = self.jump_force
            self.is_on_floor = False

        # 3. APLICAR ACELERACIÓN (Gravedad)
        # La gravedad aumenta la velocidad hacia abajo con el tiempo
        if not self.is_on_floor:
            self.velocity_y += self.gravity_force * fps_factor * dt
        
        # 4. ACTUALIZAR POSICIÓN Y
        entity.y += self.velocity_y * fps_factor * dt

    def set_gravity_status(self, status: bool):
        """Permite activar o desactivar la gravedad en tiempo real."""
        self.gravity_enabled = status
        if not status:
            self.velocity_y = 0