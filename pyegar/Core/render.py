# pyegar/Node/Windows/win/render.py (o la ruta donde lo tengas)
import pygame

def draw_node(screen, node, camera=None):
    """
    Procesador universal de renderizado.
    Maneja el dibujo de texturas y formas geométricas con soporte de cámara.
    """
    
    # 1. Obtener posición base (Mundo)
    render_x, render_y = node.x, node.y

    # 2. Aplicar desplazamiento de cámara (Si existe)
    if camera:
        render_x, render_y = camera.apply(render_x, render_y)

    # 3. MODO DIBUJO GEOMÉTRICO (Prioridad en V0.5)
    # Si el nodo tiene el componente 'Draw' activo
    if hasattr(node, 'eg_draw'):
        node.eg_draw.x, node.eg_draw.y = render_x, render_y
        # El componente Draw ya tiene su propia lógica de dibujo sobre la pantalla

    # 4. MODO TEXTURA / SPRITE
    # Solo se ejecuta si el nodo tiene una textura cargada
    if hasattr(node, 'texture') and node.texture is not None:
        rect = node.texture.get_rect()
        
        # Manejo de dimensiones personalizadas
        if hasattr(node, 'width') and hasattr(node, 'height'):
            if node.width != rect.width or node.height != rect.height:
                temp_texture = pygame.transform.scale(node.texture, (int(node.width), int(node.height)))
                rect = temp_texture.get_rect()
            else:
                temp_texture = node.texture
        else:
            temp_texture = node.texture

        # Posicionamiento centrado
        rect.center = (int(render_x), int(render_y))

        # Dibujo final del Sprite
        screen.blit(temp_texture, rect)

    # 5. DIBUJO DE HITBOX (Depuración)
    # Si el motor tiene activado el modo debug, dibujamos el borde de la colisión
    if hasattr(node, 'eg_collision') and node.eg_collision.color:
        node.eg_collision._update_collision(render_x, render_y)
        node.eg_collision._draw_collision(screen)

def is_on_screen(node, screen_width, screen_height, camera=None):
    """
    Culling: Verifica si un objeto es visible para no gastar recursos.
    """
    # Si no hay cámara, asumimos límites de la pantalla
    offset_x = camera.offset_x if camera else 0
    offset_y = camera.offset_y if camera else 0
    
    if (node.x - offset_x > screen_width + 100 or node.x - offset_x < -100 or
        node.y - offset_y > screen_height + 100 or node.y - offset_y < -100):
        return False
    return True