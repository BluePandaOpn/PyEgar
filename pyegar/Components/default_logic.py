# pyegar/Components/Default/default_logic.py
import pygame

def move_logic(x, y, speed, dt):
    """
    Gestiona la lógica de movimiento direccional (Ejes X e Y) 
    sincronizada con el Delta Time del motor.
    
    Args:
        x, y (float): Posición actual.
        speed (float): Píxeles por segundo (ej: 300).
        dt (float): Tiempo real transcurrido (proporcionado por Wind.py).
        
    Returns:
        tuple: (nueva_x, nueva_y, dir_x, dir_y)
    """
    keys = pygame.key.get_pressed()
    
    # Direcciones de movimiento (útiles para el auto-flip de Sprites)
    x_dir = 0
    y_dir = 0

    # 1. CÁLCULO DE MAGNITUD
    # Multiplicamos la velocidad por el tiempo para obtener la distancia real.
    # Esto asegura que el personaje recorra 'speed' píxeles en 1 segundo exacto.
    distancia = speed * dt

    # 2. PROCESAMIENTO EJE X (Horizontal)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= distancia
        x_dir = -1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += distancia
        x_dir = 1

    # 3. PROCESAMIENTO EJE Y (Vertical)
    # Nota: En juegos Top-Down se usa para caminar; en Platformers se ignora 
    # si Gravity2D está activo (ya que Gravity maneja el salto).
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= distancia
        y_dir = -1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += distancia
        y_dir = 1

    return x, y, x_dir, y_dir