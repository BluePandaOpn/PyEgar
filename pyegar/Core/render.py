import pygame

def draw_node(screen, node, camera=None):
    """
    Procesa el dibujado de un nodo en pantalla.
    Maneja texturas, transformaciones y desplazamiento de cámara.
    """
    
    # 1. Verificar si el nodo tiene una textura válida para dibujar
    if not hasattr(node, 'texture') or node.texture is None:
        return

    # 2. Obtener la posición base
    render_x, render_y = node.x, node.y

    # 3. Aplicar el desplazamiento de la cámara (si existe)
    if camera:
        # Usamos el método apply del nodo Camera2D para transformar coordenadas mundo -> pantalla
        render_x, render_y = camera.apply(render_x, render_y)

    # 4. Manejo del Pivote (Centrado del Sprite)
    # Por defecto, PyEgar dibuja desde el centro para facilitar rotaciones y colisiones
    rect = node.texture.get_rect()
    
    # Si el nodo tiene dimensiones personalizadas, escalamos la imagen
    if hasattr(node, 'width') and hasattr(node, 'height'):
        if node.width != rect.width or node.height != rect.height:
            # Nota: El escalado en cada frame es costoso. 
            # Es mejor que Sprite2D cachee la textura escalada.
            temp_texture = pygame.transform.scale(node.texture, (int(node.width), int(node.height)))
            rect = temp_texture.get_rect()
        else:
            temp_texture = node.texture
    else:
        temp_texture = node.texture

    # Centramos el rect en las coordenadas de renderizado
    rect.center = (int(render_x), int(render_y))

    # 5. Manejo de Rotación (Opcional si el nodo tiene atributo 'rotation')
    if hasattr(node, 'rotation') and node.rotation != 0:
        rotated_texture = pygame.transform.rotate(temp_texture, node.rotation)
        new_rect = rotated_texture.get_rect(center=rect.center)
        screen.blit(rotated_texture, new_rect)
    else:
        # Dibujo estándar
        screen.blit(temp_texture, rect)

def is_on_screen(node, camera, screen_width, screen_height):
    """
    Culling: Verifica si un objeto está dentro de la visión de la cámara.
    Si devuelve False, el motor puede saltarse el renderizado para ganar FPS.
    """
    if not camera: return True
    
    view_x, view_y = camera.apply(node.x, node.y)
    margin = 100 # Margen de seguridad
    
    return (view_x > -margin and view_x < screen_width + margin and
            view_y > -margin and view_y < screen_height + margin)