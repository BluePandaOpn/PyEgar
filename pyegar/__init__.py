# pyegar/__init__.py
import pygame
import inspect
import functools

# 1. INICIALIZACIÓN DEL CENTINELA DE SEGURIDAD (ERROREGAS)
# Importamos e iniciamos antes que cualquier otra lógica interna
try:
    from .Components.ErrorEgar.erroregas import ERROREGAS
    ERROREGAS.start()
except ImportError:
    print(">>> [PyEgar Warning] No se pudo encontrar la librería ERROREGAS.")

# 2. IMPORTACIONES DE SUBMÓDULOS DEL NÚCLEO
from .Node.Windows.win.Wind import win, init, render
from .Node.Node2D.CharacterBody.Character import CharacterBody2D
from .Node.Node2D.CollisionShaper2D.Collision import CollisionShape2D
from .Components.Physics.Gravity import Gravity2D
from .Node.Control.Label2D.Label import Label
from .Node.Node2D.Sprite2D.Sprite import Sprite2D
from .Components.draw.draw import Draw
from .Resources.colors import *

print(">>> [PyEgar Kernel V0.3] Sistema cargado. Centinela ERROREGAS en línea.")

# --- DECORADORES DE SEGURIDAD PYEGAR ---

def private(func):
    """Restringe el acceso a la función para que sea tratada como interna."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_private = True
    return wrapper

def public(func):
    """Marca explícitamente una función como parte de la API pública."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_private = False
    return wrapper

def const(name, value, target):
    """Crea una propiedad de solo lectura en el objeto (Constante)."""
    # Usamos property para que no se pueda sobrescribir
    setattr(target.__class__, name, property(lambda self: value))

def eg_import(target, source_obj, func_name):
    """Importa selectivamente una función pública de otro objeto."""
    func = getattr(source_obj, func_name)
    if hasattr(func, "_is_private") and func._is_private:
        print(f"PyEgar Error: No se puede importar '{func_name}', es @private.")
    else:
        setattr(target, func_name, func)

# --- CLASE DE INYECCIÓN DE NODOS (LIBS) ---

class libs:
    def __init__(self, target, *components):
        """
        Inyecta componentes y asegura que 'target' sea el dueño absoluto de los atributos.
        """
        # 1. INICIALIZACIÓN DEL NÚCLEO EN EL TARGET
        if not hasattr(target, 'x'): target.x = 0
        if not hasattr(target, 'y'): target.y = 0
        
        # El motor de dibujo y estados viven directamente en el target
        target.eg_draw = Draw()
        target.has_collision = False
        target.eg_collision = None

        # 2. INYECCIÓN DINÁMICA DE COMPONENTES
        for component in components:
            # Transferimos funciones al target vinculándolas a su propia instancia
            for name, method in inspect.getmembers(component, predicate=inspect.isfunction):
                if not name.startswith("__") or name == "__init__":
                    # Vinculamos el método al target para que 'self' sea el objeto destino
                    setattr(target, name, method.__get__(target, target.__class__))
            
            # Ejecutamos el constructor del componente sobre el target para inicializar variables
            component.__init__(target)

        # 3. CONFIGURACIÓN AUTOMÁTICA DE COLISIONES
        if any(c.__name__ == 'CollisionShape2D' for c in components):
            target.has_collision = True
            target.eg_collision = CollisionShape2D()

        # 4. VINCULACIÓN DEL RENDERIZADOR (PIPELINE DE ACTUALIZACIÓN)
        def _update_all_logic(entity, screen):
            """Lógica interna para actualizar todos los nodos inyectados en orden."""
            # Sincronizar motor de dibujo
            entity.eg_draw._update_screen(screen)
            entity.eg_draw.x, entity.eg_draw.y = entity.x, entity.y

            # Ejecutar actualizaciones de cada capa física/gráfica
            if hasattr(entity, '_apply_gravity'): 
                entity._apply_gravity(entity)
            
            if hasattr(entity, '_internal_body_update'): 
                entity._internal_body_update(screen)
            
            if hasattr(entity, '_draw_sprite'): 
                entity._draw_sprite(screen, entity)
            
            if hasattr(entity, '_internal_label_update'): 
                entity._internal_label_update(screen)

            # Sincronizar hitbox con la posición actual
            if entity.has_collision and entity.eg_collision:
                entity.eg_collision._update_collision(entity.x, entity.y)

            # Ejecutar el dibujo personalizado del usuario si existe
            if hasattr(entity, "on_draw"): 
                entity.on_draw()

        # Inyectamos la función anterior en el target para que Wind.py pueda llamarla
        target._update_all = _update_all_logic.__get__(target, target.__class__)