# pyegar/Node/Node2D/CollisionShaper2D/Collision.py
import pygame

class CollisionShape2D:
    def __init__(self):
        # El objeto Rect de Pygame que maneja la física real (Coordenadas de Mundo)
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
        """Define el tamaño de la caja de colisión y un color de borde opcional para debug."""
        self.hitbox.width = width
        self.hitbox.height = height
        self.color = color

    def set_drag(self, status: bool):
        """Activa o desactiva la capacidad de arrastrar con el ratón."""
        self.drag_enabled = status

    def _update_collision(self, x, y):
        """Actualiza la posición del Rect basándose en la entidad (Uso interno)."""
        self.hitbox.x = int(x)
        self.hitbox.y = int(y)

    def _draw_collision(self, screen, camera=None):
        """
        Dibuja el borde de la hitbox si se definió un color.
        Soporta desplazamiento de cámara para que el debug sea preciso.
        """
        if self.color:
            if camera:
                # Si hay cámara, dibujamos un rectángulo temporal en la posición de pantalla
                render_x, render_y = camera.apply(self.hitbox.x, self.hitbox.y)
                draw_rect = pygame.Rect(render_x, render_y, self.hitbox.width, self.hitbox.height)
                pygame.draw.rect(screen, self.color, draw_rect, 2)
            else:
                # Dibujo normal si no hay cámara
                pygame.draw.rect(screen, self.color, self.hitbox, 2)

    # --- DETECCIÓN DE COLISIONES ---

    def is_colliding_with(self, other_collision):
        """
        Compara la hitbox actual con la de otro objeto.
        Uso: if player.eg_collision.is_colliding_with(enemy.eg_collision):
        """
        if hasattr(other_collision, 'hitbox'):
            return self.hitbox.colliderect(other_collision.hitbox)
        return False

    def is_hover(self):
        """Detecta si el mouse está sobre la colisión."""
        mouse_pos = pygame.mouse.get_pos()
        return self.hitbox.collidepoint(mouse_pos)

    # --- LÓGICA DE ARRASTRE (DRAG & DROP) ---

    def update_drag(self, entity):
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

        # Aplicar movimiento
        if self._dragging:
            entity.x = mouse_pos[0] + self._offset_x
            entity.y = mouse_pos[1] + self._offset_y
            
        return self._dragging