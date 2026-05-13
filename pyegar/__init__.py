# V0.5
# pyegar/__init__.py
import pygame
import inspect
import functools
import time
import sys
from colorama import init as colorama_init

# --- 1. INICIALIZACIÓN DEL CENTINELA ---
try:
    from .Components.erroregas import ERROREGAS
    ERROREGAS.start()
except ImportError:
    pass

# --- 2. ANIMACIÓN DE CARGA (KERNEL BOOT) ---
def boot_animation():
    colorama_init(autoreset=True)
    frames = ["|", "/", "-", "\\"]
    sys.stdout.write("\033[94m>>> [Kernel V0.5] Compilando módulos ")
    for i in range(12):
        time.sleep(0.05)
        sys.stdout.write(f"\r\033[94m>>> [Kernel V0.5] Compilando módulos {frames[i % 4]} {'.' * (i//3)}")
        sys.stdout.flush()
    sys.stdout.write(f"\r\033[92m>>> [Kernel V0.5] SISTEMA LISTO PARA RENDERIZAR.          \n")
    print("-" * 50)

boot_animation()

# --- 3. IMPORTACIONES DEL NÚCLEO ---
from .Node.Windows.Wind import win, init, render, _SCENE_MASTER
from .Node.Node2D.Character import CharacterBody2D
from .Node.Node2D.Collision import CollisionShape2D
from .Node.Node2D.camera import Camera2D
from .Node.Node2D.Sprite import Sprite2D
from .Node.Control.Label import Label
from .Components.Gravity import Gravity2D
from .Components.draw import Draw
from .Resources.colors import *

# --- 4. PROCESADOR DE LÓGICA ANTI-RECURSIÓN ---
def _core_processor(entity, screen):
    """
    Maneja la actualización de componentes sin disparar el on_draw
    evitando así el RecursionError.
    """
    # 1. Sincronizar sistema de dibujo
    if hasattr(entity, 'eg_draw'):
        # Llamada estática para máxima eficiencia
        Draw._update_screen(entity.eg_draw, screen)
        entity.eg_draw.x, entity.eg_draw.y = entity.x, entity.y

    # 2. Ejecutar físicas y lógica interna
    # Solo ejecutamos métodos internos (que empiezan con _)
    metodos = dir(entity)
    
    if '_apply_gravity' in metodos:
        entity._apply_gravity(entity)
        
    if '_internal_body_update' in metodos:
        entity._internal_body_update(screen)
        
    if '_draw_sprite' in metodos:
        entity._draw_sprite(screen, entity)

    # 3. Sincronizar colisiones
    if getattr(entity, 'has_collision', False) and entity.eg_collision:
        entity.eg_collision._update_collision(entity.x, entity.y)

# --- 5. CLASE MAESTRA DE INYECCIÓN (LIBS) ---
class libs:
    def __init__(self, target, *components):
        # Validación de integridad
        if 'ERROREGAS' in globals():
            ERROREGAS.validate_injection(target, components)

        # Atributos base obligatorios
        if not hasattr(target, 'x'): target.x = 0.0
        if not hasattr(target, 'y'): target.y = 0.0
        
        target.eg_draw = Draw()
        target.has_collision = False
        target.eg_collision = None
        
        if not hasattr(target, '_eg_state'):
            target._eg_state = {"dt": 0.0}

        # Registro de Escenas
        target.scene = lambda name: _SCENE_MASTER.scenes.update({name: target})

        # Inyección de métodos de componentes
        for component in components:
            for name, method in inspect.getmembers(component, predicate=inspect.isfunction):
                if not name.startswith("__") or name == "__init__":
                    setattr(target, name, method.__get__(target, target.__class__))
            component.__init__(target)

        # Configurar sistema de colisiones si se inyectó la clase
        if any(c.__name__ == 'CollisionShape2D' for c in components):
            target.has_collision = True
            target.eg_collision = CollisionShape2D()

        # Vinculación del pipeline
        # Usamos una lambda limpia para que no se guarde el contexto de la escena
        target._update_all = lambda screen: _core_processor(target, screen)

# --- 6. DECORADORES ---
def private(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    wrapper._is_private = True
    return wrapper

def public(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    wrapper._is_private = False
    return wrapper