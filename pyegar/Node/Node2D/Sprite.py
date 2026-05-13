# pyegar/Node/Node2D/Sprite2D/Sprite.py
import pygame

class Sprite2D:
    def __init__(self):
        self.texture = None
        self.rect_sprite = None
        self._flip_x = False
        
        # Dimensiones para el renderizador
        self.width = 0
        self.height = 0

    def load_texture(self, path, width=None, height=None):
        """
        Carga una imagen y la optimiza para el motor.
        """
        try:
            # .convert_alpha() mejora mucho el rendimiento en Pygame
            self.texture = pygame.image.load(path).convert_alpha()
            
            # Si no se dan dimensiones, usamos las originales de la imagen
            self.width = width if width else self.texture.get_width()
            self.height = height if height else self.texture.get_height()

            # Escalado inicial (solo se hace una vez para ahorrar CPU)
            self.texture = pygame.transform.scale(self.texture, (int(self.width), int(self.height)))
            self.rect_sprite = self.texture.get_rect()
            
        except Exception as e:
            print(f">>> [PyEgar Error] No se pudo cargar la imagen en: {path}")

    def flip(self, horizontal=False):
        """Voltea la imagen manualmente."""
        self._flip_x = horizontal

    def _draw_sprite(self, screen, entity):
        """
        Este método es invocado internamente por el motor.
        Prepara la textura según la dirección del movimiento.
        """
        if self.texture is None:
            return

        # 1. DIRECCIÓN AUTOMÁTICA
        # Si el personaje se mueve a la izquierda, volteamos la imagen
        if hasattr(entity, 'x_direction'):
            if entity.x_direction < 0:
                self._flip_x = True
            elif entity.x_direction > 0:
                self._flip_x = False

        # 2. PROCESAMIENTO DE VOLTEO
        # Creamos una vista temporal si hay volteo (no modifica la textura original)
        render_img = pygame.transform.flip(self.texture, self._flip_x, False)
        
        # 3. SINCRONIZACIÓN CON EL NODO
        # El render.py usará entity.texture para dibujar
        entity.texture = render_img
        
        # NOTA: El dibujado real lo hace ahora render.py usando el offset de la cámara.