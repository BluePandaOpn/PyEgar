# pyegar/Node/Node2D/Camera2D/camera.py
import pygame

class Camera2D:
    def __init__(self):
        # Propiedades de posición (Offset en el mundo)
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # Configuración de comportamiento
        self.target = None      # Objeto a seguir (ej: el jugador)
        self.smoothing = 0.1    # Suavizado de movimiento (Lerp)
        self.zoom = 1.0         # Reservado para futuras versiones
        
        # Límites del mundo (para que la cámara no muestre el vacío)
        self.limit_left = -10000
        self.limit_right = 10000
        self.limit_top = -10000
        self.limit_bottom = 10000

    def follow(self, entity):
        """Asigna una entidad para que la cámara la siga de forma automática."""
        self.target = entity

    def apply(self, x, y):
        """
        Transforma una coordenada del MUNDO a una coordenada de PANTALLA.
        Se usa dentro del renderizador para saber dónde dibujar.
        """
        return x - self.offset_x, y - self.offset_y

    def update(self, screen_width, screen_height):
        """
        Calcula el desplazamiento necesario para centrar el objetivo.
        Debe llamarse en cada frame antes de dibujar los objetos.
        """
        if self.target:
            # 1. Calculamos el centro del objetivo (asumiendo que tiene ancho/alto)
            # Si no los tiene, usamos 0 como fallback
            t_w = getattr(self.target, 'ancho', getattr(self.target, 'width', 0))
            t_h = getattr(self.target, 'alto', getattr(self.target, 'height', 0))
            
            target_center_x = self.target.x + (t_w / 2)
            target_center_y = self.target.y + (t_h / 2)

            # 2. Destino ideal: El centro del target menos la mitad de la pantalla
            dest_x = target_center_x - (screen_width / 2)
            dest_y = target_center_y - (screen_height / 2)

            # 3. Aplicamos suavizado (Interpolación Lineal)
            # Esto hace que la cámara no se mueva bruscamente
            self.offset_x += (dest_x - self.offset_x) * self.smoothing
            self.offset_y += (dest_y - self.offset_y) * self.smoothing

            # 4. Restricción de límites del mapa
            self.offset_x = max(self.limit_left, min(self.offset_x, self.limit_right - screen_width))
            self.offset_y = max(self.limit_top, min(self.offset_y, self.limit_bottom - screen_height))

    def set_limits(self, left, top, right, bottom):
        """Define los bordes máximos que la cámara puede alcanzar."""
        self.limit_left = left
        self.limit_top = top
        self.limit_right = right
        self.limit_bottom = bottom