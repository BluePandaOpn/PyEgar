import pygame
import sys
import __main__

# Pantalla global del motor
_current_screen = None
# Variable interna para rastrear el tiempo delta
_delta_time = 0.0

def init():
    """
    Inicializa el motor PyEgar extrayendo la configuración 
    directamente del script principal del usuario.
    """
    global _current_screen
    pygame.init()
    
    # Extraer configuración del __main__ con fallbacks de seguridad
    W = getattr(__main__, 'WIDTH', 800)
    H = getattr(__main__, 'HEIGHT', 600)
    T = getattr(__main__, 'TITLE', "PyEgar Engine")
    F = getattr(__main__, 'FPS', 60)
    
    _current_screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(T)
    
    print(f">>> [PyEgar Wind] Ventana iniciada: {W}x{H} @ {F} FPS")
    
    return {
        "clock": pygame.time.Clock(), 
        "fps": F
    }

def render(node):
    """
    Renderiza un nodo y actualiza su bus de datos con el Delta Time actual.
    """
    global _delta_time
    if _current_screen and node:
        # Sincronizamos el dt en el bus de datos del nodo antes de actualizar
        if hasattr(node, '_eg_state'):
            node._eg_state["dt"] = _delta_time
            
        # Ejecutamos el pipeline de actualización de libs
        node._update_all(_current_screen)

class win:
    def __init__(self, config):
        self.clock = config["clock"]
        self.fps = config["fps"]
        self.run = True

    def main_logic(self):
        """Método destinado a ser sobreescrito por el usuario."""
        pass

    def start(self):
        """
        Bucle principal del motor. 
        Gestiona el tiempo delta, eventos y el refresco de pantalla.
        """
        global _delta_time
        
        while self.run:
            # 1. CÁLCULO DE DELTA TIME (Segundos transcurridos desde el último frame)
            # tick() devuelve milisegundos; dividimos por 1000 para obtener segundos.
            milli = self.clock.tick(self.fps)
            _delta_time = milli / 1000.0

            # 2. LIMPIEZA DE PANTALLA (Fondo oscuro por defecto)
            _current_screen.fill((30, 30, 30))
            
            # 3. GESTIÓN DE EVENTOS BÁSICOS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            # 4. LÓGICA DE USUARIO Y RENDERIZADO
            self.main_logic()
            
            # 5. ACTUALIZACIÓN DINÁMICA
            pygame.display.flip()
            
        # Cierre seguro del sistema
        pygame.quit()
        sys.exit()