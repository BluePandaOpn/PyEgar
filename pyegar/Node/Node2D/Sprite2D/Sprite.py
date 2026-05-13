import pygame

class Sprite2D:
    def __init__(self):
        self.texture = None
        self.rect_sprite = None
        self._flip_x = False

    def load_texture(self, path, width=None, height=None):
        """
        Carga una imagen y opcionalmente le cambia el tamaño.
        Uso: self.load_texture("Player.png", 64, 64)
        """
        try:
            # .convert_alpha() es vital para que las transparencias de los PNG funcionen
            self.texture = pygame.image.load(path).convert_alpha()
            
            if width and height:
                self.texture = pygame.transform.scale(self.texture, (width, height))
            
            self.rect_sprite = self.texture.get_rect()
        except Exception as e:
            print(f"PyEgar Error: No se pudo cargar la textura en '{path}'. {e}")

    def flip(self, horizontal=False):
        """Permite forzar el volteo manualmente si el usuario lo desea."""
        self._flip_x = horizontal

    def _draw_sprite(self, screen, entity):
        """
        Renderiza la imagen en la pantalla.
        Detecta automáticamente la dirección si la entidad tiene 'x_direction'.
        """
        # Si no hay textura cargada, salimos silenciosamente para no dar error
        if self.texture is None:
            return

        # --- Lógica de Dirección Automática ---
        # Si el objeto tiene x_direction (inyectado por CharacterBody2D)
        if hasattr(entity, 'x_direction'):
            if entity.x_direction < 0:
                self._flip_x = True   # Mirar a la izquierda (Espejo)
            elif entity.x_direction > 0:
                self._flip_x = False  # Mirar a la derecha (Normal)

        # Crear la versión volteada (o no) de la textura
        render_img = pygame.transform.flip(self.texture, self._flip_x, False)

        # Dibujar en las coordenadas actuales de la entidad
        screen.blit(render_img, (entity.x, entity.y))