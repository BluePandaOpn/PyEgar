# pyegar/Components/draw/draw.py
import pygame

class Draw:
    def __init__(self):
        self._screen = None
        # Coordenadas locales (sincronizadas con el nodo padre)
        self.x = 0.0
        self.y = 0.0

    def _update_screen(self, screen):
        """Actualiza la referencia de la superficie de dibujo (Uso interno)."""
        self._screen = screen

    def _get_render_pos(self, camera=None):
        """
        Calcula la posición final de dibujo aplicando la cámara si existe.
        """
        if camera:
            return camera.apply(self.x, self.y)
        return self.x, self.y

    def rect(self, width, height, color=(255, 255, 255), camera=None):
        """
        Dibuja un rectángulo sólido.
        Soporta paso de cámara para posicionamiento dinámico.
        """
        if self._screen:
            rx, ry = self._get_render_pos(camera)
            pygame.draw.rect(self._screen, color, (int(rx), int(ry), int(width), int(height)))

    def circle(self, radius, color=(255, 255, 255), camera=None):
        """
        Dibuja un círculo. La posición x, y actúa como el centro.
        """
        if self._screen:
            rx, ry = self._get_render_pos(camera)
            pygame.draw.circle(self._screen, color, (int(rx), int(ry)), int(radius))

    def line(self, start_pos, end_pos, width=1, color=(255, 255, 255), camera=None):
        """
        Dibuja una línea. Si se pasa cámara, se ajustan ambos puntos.
        """
        if self._screen:
            if camera:
                s_x, s_y = camera.apply(start_pos[0], start_pos[1])
                e_x, e_y = camera.apply(end_pos[0], end_pos[1])
                pygame.draw.line(self._screen, color, (s_x, s_y), (e_x, e_y), width)
            else:
                pygame.draw.line(self._screen, color, start_pos, end_pos, width)

    def polygon(self, points, color=(255, 255, 255), camera=None):
        """
        Dibuja un polígono personalizado (útil para triángulos o formas raras).
        """
        if self._screen:
            if camera:
                new_points = [camera.apply(p[0], p[1]) for p in points]
                pygame.draw.polygon(self._screen, color, new_points)
            else:
                pygame.draw.polygon(self._screen, color, points)