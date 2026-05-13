# PyEgar/Components/Default/default_logic.py
import pygame

def move_logic(x, y, speed, dt):
    """
    Gestiona la lógica de movimiento direccional utilizando Delta Time.
    
    Args:
        x (float): Posición actual en el eje X.
        y (float): Posición actual en el eje Y.
        speed (float): Velocidad base (píxeles por segundo).
        dt (float): Tiempo transcurrido desde el último frame (Delta Time).
        
    Returns:
        tuple: (nueva_x, nueva_y, x_dir, y_dir)
    """
    keys = pygame.key.get_pressed()
    x_dir = 0
    y_dir = 0

    # Calculamos el desplazamiento real multiplicando la velocidad por dt.
    # Esto garantiza que el objeto recorra 'speed' píxeles en exactamente 1 segundo.
    move_amount = speed * dt

    # --- Movimiento Horizontal (WASD / Flechas) ---
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= move_amount
        x_dir = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += move_amount
        x_dir = 1

    # --- Movimiento Vertical (WASD / Flechas) ---
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= move_amount
        y_dir = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += move_amount
        y_dir = 1

    # Retornamos las nuevas posiciones y las direcciones para los Sprites
    return x, y, x_dir, y_dir