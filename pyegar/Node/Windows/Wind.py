import pygame
import sys
import __main__

# --- VARIABLES DE CONTROL INTERNAS ---
_current_screen = None
_delta_time = 0.0

def init():
    """
    Inicializa el hardware y configura la ventana extrayendo 
    datos del script principal.
    """
    global _current_screen
    pygame.init()
    
    # Extraer configuración del __main__ (Script del usuario)
    W = getattr(__main__, 'WIDTH', 800)
    H = getattr(__main__, 'HEIGHT', 600)
    T = getattr(__main__, 'TITLE', "PyEgar Engine V0.5")
    F = getattr(__main__, 'FPS', 60)
    
    _current_screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(T)
    
    print(f">>> [PyEgar Wind] Motor V0.5 Iniciado: {W}x{H} @ {F} FPS")
    
    return {
        "clock": pygame.time.Clock(), 
        "fps": F
    }

class SceneManager:
    """Gestiona el cambio y la ejecución de pantallas/niveles."""
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def set_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            print(f">>> [PyEgar Error] La escena '{name}' no ha sido registrada.")

# Instancia única para todo el motor
_SCENE_MASTER = SceneManager()

def render(node):
    """
    Función central de procesamiento.
    1. Si recibe un String: Cambia la escena activa.
    2. Si recibe un Objeto: Procesa sus físicas y activa su pipeline de dibujo.
    """
    global _delta_time, _current_screen
    
    # Cambio de escena: render("Nombre")
    if isinstance(node, str):
        _SCENE_MASTER.set_scene(node)
        return

    # Procesamiento de objeto
    if _current_screen and node:
        # Inyectar Delta Time para cálculos físicos precisos
        if hasattr(node, '_eg_state'):
            node._eg_state["dt"] = _delta_time
            
        # Llamar al pipeline de actualización (inyectado por libs en __init__.py)
        if hasattr(node, '_update_all'):
            node._update_all(_current_screen)

class win:
    def __init__(self, config):
        self.clock = config["clock"]
        self.fps = config["fps"]
        self.run = True

    def start(self):
        """
        Bucle Maestro del Motor.
        Controla el tiempo, eventos, limpieza de buffer y renderizado de escenas.
        """
        global _delta_time, _current_screen
        
        while self.run:
            # 1. GESTIÓN DE TIEMPO (Delta Time)
            # Calculamos los segundos exactos entre frames para que el movimiento sea fluido
            milli = self.clock.tick(self.fps)
            _delta_time = milli / 1000.0

            # 2. LIMPIEZA DE PANTALLA (Fondo base)
            _current_screen.fill((30, 30, 30))
            
            # 3. GESTIÓN DE EVENTOS DE SISTEMA
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            # 4. EJECUCIÓN DE LA ESCENA ACTIVA
            # Si hay una escena seleccionada, ejecutamos su método on_draw()
            if _SCENE_MASTER.current_scene:
                if hasattr(_SCENE_MASTER.current_scene, "on_draw"):
                    _SCENE_MASTER.current_scene.on_draw()
            
            # 5. ACTUALIZACIÓN DE PANTALLA
            pygame.display.flip()
            
        # Salida limpia
        pygame.quit()
        sys.exit()