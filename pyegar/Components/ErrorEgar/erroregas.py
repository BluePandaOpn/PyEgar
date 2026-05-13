import sys
import traceback
import os
import webbrowser

class ERROREGAS:
    # Definición de Capas Técnicas
    NODE2D_ERROR = "CAPA_NODE_2D"    # Errores en Character, Sprite, Collision
    WIN_ERROR    = "CAPA_SISTEMA_WIN" # Errores en Wind.py o resolución
    SYNTAX_ERROR = "CAPA_SINTAXIS"    # Errores de escritura del usuario

    GITHUB_DOCS = "https://github.com/Pato404/PyEgar/wiki/"

    @staticmethod
    def start():
        sys.excepthook = ERROREGAS.analyze
        # No imprimimos mucho aquí para mantener la consola limpia

    @staticmethod
    def analyze(exctype, value, tb):
        stack = traceback.extract_tb(tb)
        last_call = stack[-1]
        
        file_path = last_call.filename
        line_no = last_call.lineno
        code_context = last_call.line
        
        # Lógica de detección de capa por ruta de archivo
        category = ERROREGAS.SYNTAX_ERROR
        path_lower = file_path.lower()

        if "node2d" in path_lower or "components" in path_lower:
            category = ERROREGAS.NODE2D_ERROR
        elif "windows" in path_lower or "win" in path_lower:
            category = ERROREGAS.WIN_ERROR

        # Dibujar reporte en consola (puedes usar el diseño anterior)
        ERROREGAS.render_report(category, exctype.__name__, value, file_path, line_no, code_context)
        
        # Abrir Wiki de GitHub
        webbrowser.open(f"{ERROREGAS.GITHUB_DOCS}{category}#{exctype.__name__}")
        sys.exit(1)

    @staticmethod
    def render_report(cat, name, val, file, line, code):
        # Colores según capa
        c = "\033[91m" # Rojo
        if cat == ERROREGAS.NODE2D_ERROR: c = "\033[94m" # Azul
        if cat == ERROREGAS.WIN_ERROR:    c = "\033[93m" # Amarillo

        print(f"\n{c}{'='*60}")
        print(f" [ERROREGAS DIAGNOSIS] -> {cat}")
        print(f"{'='*60}\033[0m")
        print(f"TIPO: {name}\nMSG:  {val}")
        print(f"FILE: {os.path.basename(file)} (Línea {line})")
        print(f"\033[90m>>> {code}\033[0m")
        print(f"{c}{'='*60}\033[0m\n")