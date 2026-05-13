from pyegar import *

# --- CONFIGURACIÓN DEL MOTOR ---
# El Kernel v0.4 lee estas variables automáticamente
WIDTH = 1000
HEIGHT = 600
TITLE = "PyEgar v0.4 | Camera Test"
FPS = 60

# --- CLASES DEL JUEGO ---

class Jugador:
    def __init__(self):
        # Inyectamos las librerías necesarias
        libs(self, CharacterBody2D, Sprite2D)
        
        # Configuración visual
        self.load_texture("player.png")
        self.x = 500
        self.y = 300
        
        # Configuración de movimiento
        self.eg_Speed(300) # Píxeles por segundo

    def update(self):
        # El nodo CharacterBody2D ya tiene controles automáticos si llamas a mov()
        self.mov()

class Mundo:
    def __init__(self):
        libs(self, Sprite2D)
        self.load_texture("background.png")
        self.x = 0
        self.y = 0
        # Hacemos el mundo muy grande para probar la cámara
        self.width = 5000 
        self.height = 2000

# --- LÓGICA PRINCIPAL ---

class MiJuego(win):
    def __init__(self, config):
        super().__init__(config)
        
        # 1. Instanciar objetos
        self.mapa = Mundo()
        self.player = Jugador()
        
        # 2. Configurar la Cámara (Novedad v0.4)
        # Inyectamos Camera2D en la instancia de win o en un nodo aparte
        libs(self, Camera2D)
        
        self.follow(self.player) # La cámara seguirá al jugador
        self.smoothing = 0.05    # Qué tan suave es el movimiento (0.01 a 1.0)
        
        # Registramos esta cámara en el motor
        set_camera(self)

    def main_logic(self):
        """Este método se ejecuta en cada frame"""
        # Actualizar lógica de los objetos
        self.player.update()
        
        # Renderizar (el motor aplicará el offset de cámara automáticamente)
        render(self.mapa)
        render(self.player)

# --- ARRANQUE ---
if __name__ == "__main__":
    engine_config = init()
    app = MiJuego(engine_config)
    app.start()