import pygame

class Draw:
    def __init__(self):
        self._screen = None
        self.x = 0
        self.y = 0

    def _update_screen(self, screen):
        """Actualiza la referencia de la pantalla (Uso interno)."""
        self._screen = screen

    def rect(self, width, height, color=(255, 255, 255)):
        """Dibuja un rectángulo sólido en la posición del objeto."""
        if self._screen:
            pygame.draw.rect(self._screen, color, (self.x, self.y, width, height))

    def circle(self, radius, color=(255, 255, 255)):
        """Dibuja un círculo en la posición del objeto."""
        if self._screen:
            # Dibujamos el círculo usando x, y como centro
            pygame.draw.circle(self._screen, color, (int(self.x), int(self.y)), radius)

    def line(self, start_pos, end_pos, width=1, color=(255, 255, 255)):
        """Dibuja una línea."""
        if self._screen:
            pygame.draw.line(self._screen, color, start_pos, end_pos, width)