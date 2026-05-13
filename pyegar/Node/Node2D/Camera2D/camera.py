# pyegar/Node/Node2D/Camera2D/camera.py

class Camera2D:
    def __init__(self):
        # Propiedades de posición (Offset en el mundo)
        self.offset_x = 0
        self.offset_y = 0
        
        # Configuración de comportamiento
        self.target = None      # Objeto a seguir
        self.smoothing = 0.1    # Velocidad de seguimiento (0.1 = suave, 1 = instantáneo)
        self.zoom = 1.0         # Nivel de acercamiento
        
        # Límites del mundo (opcional, para que no se vea el vacío)
        self.limit_left = -10000
        self.limit_right = 10000
        self.limit_top = -10000
        self.limit_bottom = 10000

    def follow(self, entity):
        """Asigna una entidad (jugador, npc, etc.) para que la cámara la siga."""
        self.target = entity

    def update(self, screen_width, screen_height):
        """Calcula el offset necesario para centrar el target en pantalla."""
        if self.target:
            # 1. Calculamos el centro del objetivo
            # Asumimos que la entidad tiene atributos .x, .y, .width y .height
            target_center_x = self.target.x + (getattr(self.target, 'width', 0) / 2)
            target_center_y = self.target.y + (getattr(self.target, 'height', 0) / 2)

            # 2. Destino ideal: El centro del target menos la mitad de la pantalla
            dest_x = target_center_x - (screen_width / 2)
            dest_y = target_center_y - (screen_height / 2)

            # 3. Aplicamos LERP (Interpolación Lineal) para el suavizado
            self.offset_x += (dest_x - self.offset_x) * self.smoothing
            self.offset_y += (dest_y - self.offset_y) * self.smoothing

            # 4. Restricción de límites (Para no salirse del mapa)
            self.offset_x = max(self.limit_left, min(self.offset_x, self.limit_right - screen_width))
            self.offset_y = max(self.limit_top, min(self.offset_y, self.limit_bottom - screen_height))

    def apply(self, x, y):
        """
        Transforma una posición global del mundo a una posición local de pantalla.
        Se usará internamente en el pipeline de renderizado.
        """
        return (x - self.offset_x) * self.zoom, (y - self.offset_y) * self.zoom