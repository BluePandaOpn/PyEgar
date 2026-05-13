import pygame

class Label:
    # Caché compartido por todas las instancias para ahorrar memoria RAM
    _font_cache = {}

    def __init__(self):
        self.text_content = ""
        self.font_size = 20
        self.text_color = (250, 250, 250)
        self.font_name = "Arial"
        
        # Posicionamiento (se sincroniza con libs)
        self.x = 0 
        self.y = 0
        self._print_x = 0
        self._print_y = 0

    def printf(self, text, size=None, color=None, x=None, y=None, font="Arial"):
        """
        Configura el texto a mostrar. Usa caché para evitar sobrecarga.
        """
        self.text_content = str(text)
        self.font_name = font
        
        if size: self.font_size = size
        if color: self.text_color = color
        
        # Prioridad de coordenadas: 1. Parámetro | 2. Atributo del objeto
        self._print_x = x if x is not None else self.x
        self._print_y = y if y is not None else self.y

    def _get_font(self):
        """Busca la fuente en el caché o la crea si no existe."""
        key = (self.font_name, self.font_size)
        if key not in Label._font_cache:
            try:
                Label._font_cache[key] = pygame.font.SysFont(self.font_name, self.font_size)
            except Exception:
                # Fallback a fuente por defecto si falla la carga
                Label._font_cache[key] = pygame.font.Font(None, self.font_size)
        return Label._font_cache[key]

    def _internal_label_update(self, screen):
        """Renderizado optimizado que se integra en el pipeline de libs."""
        if self.text_content:
            try:
                # 1. Obtener fuente desde el caché (Ultra rápido)
                font_obj = self._get_font()
                
                # 2. Renderizar superficie de texto
                text_surface = font_obj.render(self.text_content, True, self.text_color)
                
                # 3. Dibujar en pantalla
                screen.blit(text_surface, (self._print_x, self._print_y))
            except Exception as e:
                # Integración con el concepto de ERROREGAS (opcional)
                print(f">>> [PyEgar Label Error]: {e}")