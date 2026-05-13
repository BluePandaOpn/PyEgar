from pyegar import *
import random
import time

# --- 1. CONFIGURACIÓN ---
WIDTH = 1200
HEIGHT = 800
TITLE = "PyEgar V0.5 - Memory Game"
FPS = 60

# --- 2. CLASE CUADRO ---
class Cuadro:
    def __init__(self, x, y, color_oculto):
        # Inyectamos colisión y capacidades 2D
        libs(self, CollisionShape2D)
        self.x, self.y = float(x), float(y)
        self.w, self.h = 100, 100
        
        self.color_base = (60, 60, 70)
        self.color_oculto = color_oculto
        self.color_actual = self.color_base
        
        self.revelado = False
        self.completado = False
        
        # Hitbox esencial para el hover
        self.eg_collision.rect(self.w, self.h)

    def on_draw(self):
        # Dibujamos el cuadro usando el componente eg_draw inyectado
        # Primero una sombra/borde
        self.eg_draw.rect(self.w + 6, self.h + 6, (10, 10, 15))
        # Luego el cuadro principal
        self.eg_draw.rect(self.w, self.h, self.color_actual)
        
        if self.completado:
            # Una pequeña marca de "completado"
            self.eg_draw.rect(self.w, 5, GREEN)

    def revelar(self):
        if not self.revelado:
            self.revelado = True
            self.color_actual = self.color_oculto
            return True
        return False

    def ocultar(self):
        if not self.completado:
            self.revelado = False
            self.color_actual = self.color_base

# --- 3. ESCENA PRINCIPAL ---
class MemoryGame:
    def __init__(self):
        libs(self)
        self.scene("Juego")
        
        self.cuadros = []
        self.seleccionados = []
        self.esperando = False
        self.tiempo_espera = 0
        self.mouse_lock = False
        
        colores_parejas = [RED, BLUE, GREEN, GOLD, ORANGE, PURPLE, CYAN, WHITE] * 2
        random.shuffle(colores_parejas)
        
        # Posicionamiento centrado
        for i in range(16):
            col = i % 4
            fila = i // 4
            px = 380 + (col * 120)
            py = 180 + (fila * 120)
            self.cuadros.append(Cuadro(px, py, colores_parejas[i]))

    def on_draw(self):
        # IMPORTANTE: El fondo debe ser lo primero
        self.eg_draw.rect(WIDTH, HEIGHT, (30, 30, 40))
        
        # Gestión de tiempo para fallos
        if self.esperando and time.time() > self.tiempo_espera:
            for c in self.seleccionados:
                c.ocultar()
            self.seleccionados = []
            self.esperando = False

        # Input de mouse
        mouse_press = pygame.mouse.get_pressed()[0]
        clic_detectado = False
        if mouse_press and not self.mouse_lock:
            clic_detectado = True
            self.mouse_lock = True
        if not mouse_press:
            self.mouse_lock = False

        # RENDERIZADO Y LÓGICA DE CUADROS
        for cuadro in self.cuadros:
            # 1. Ejecutar el pipeline interno (Actualiza colisiones y draw)
            render(cuadro) 
            # 2. Llamar al dibujo manual
            cuadro.on_draw()
            
            # 3. Lógica de juego
            if clic_detectado and not self.esperando and not cuadro.revelado:
                if cuadro.eg_collision.is_hover():
                    if len(self.seleccionados) < 2:
                        cuadro.revelar()
                        self.seleccionados.append(cuadro)
                        if len(self.seleccionados) == 2:
                            self.chequear_pareja()

    def chequear_pareja(self):
        c1, c2 = self.seleccionados
        if c1.color_oculto == c2.color_oculto:
            c1.completado = True
            c2.completado = True
            self.seleccionados = []
        else:
            self.esperando = True
            self.tiempo_espera = time.time() + 0.6

# --- 4. LANZAMIENTO ---
class App:
    def __init__(self):
        self.config = init()
        self.ventana = win(self.config)
        self.mundo = MemoryGame()
        render("Juego")

    def start(self):
        self.ventana.start()

if __name__ == "__main__":
    game = App()
    game.start()