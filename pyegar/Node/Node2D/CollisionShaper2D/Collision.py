import pygame

class CollisionShape2D:
    def __init__(self):
        # El objeto Rect de Pygame que maneja la física
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        
        # Propiedades visuales y de estado
        self.color = None
        self._is_pressed = False 
        self._dragging = False  
        self._offset_x = 0      
        self._offset_y = 0
        
        # Configuración de comportamiento
        self.drag_enabled = False

    def rect(self, width, height, color=None):
        """Define el tamaño de la caja de colisión y un color de borde opcional."""
        self.hitbox.width = width
        self.hitbox.height = height
        self.color = color

    def set_drag(self, status: bool):
        """Activa o desactiva la capacidad de arrastrar con el ratón."""
        self.drag_enabled = status

    def _update_collision(self, x, y):
        """Actualiza la posición del Rect (uso interno del motor)."""
        self.hitbox.x = x
        self.hitbox.y = y

    def _draw_collision(self, screen):
        """Dibuja el borde de la hitbox si se definió un color."""
        if self.color:
            pygame.draw.rect(screen, self.color, self.hitbox, 2)

    # --- DETECCIÓN DE RATÓN (MOUSE) ---

    def is_hover(self):
        """Devuelve True si el ratón está sobre el objeto."""
        return self.hitbox.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, button=0):
        """Detecta un clic único (0: Izquierdo, 1: Central, 2: Derecho)."""
        mouse_state = pygame.mouse.get_pressed()
        if self.is_hover() and mouse_state[button]:
            if not self._is_pressed:
                self._is_pressed = True
                return True
        else:
            if not mouse_state[button]:
                self._is_pressed = False
        return False

    # --- LÓGICA DE ARRASTRE (DRAG & DROP) ---

    def is_dragged(self, entity):
        """Gestiona el arrastre de la entidad. Debe llamarse en cada frame."""
        if not self.drag_enabled:
            return False

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # Iniciar arrastre
        if self.is_hover() and mouse_buttons[0] and not self._dragging:
            self._dragging = True
            self._offset_x = entity.x - mouse_pos[0]
            self._offset_y = entity.y - mouse_pos[1]

        # Finalizar arrastre
        if not mouse_buttons[0]:
            self._dragging = False

        # Aplicar movimiento con offset (para que no salte al centro)
        if self._dragging:
            entity.x = mouse_pos[0] + self._offset_x
            entity.y = mouse_pos[1] + self._offset_y
            
        return self._dragging

    # --- DETECCIÓN DE COLISIONES ENTRE OBJETOS ---

    def is_colliding_with(self, other_collision):
        """
        Compara la hitbox actual con la de otro objeto.
        Uso: if player.eg_collision.is_colliding_with(enemy.eg_collision):
        """
        if hasattr(other_collision, 'hitbox'):
            return self.hitbox.colliderect(other_collision.hitbox)
        return False

    # --- UTILIDADES VISUALES ---

    def get_auto_color(self, base_color, hover_color, drag_color):
        """Devuelve un color dinámico según el estado del ratón."""
        if self._dragging:
            return drag_color
        if self.is_hover():
            return hover_color
        return base_color