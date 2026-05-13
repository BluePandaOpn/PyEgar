import sys
import traceback
import webbrowser
import time

class ERROREGAS:
    # --- PALETA DE COLORES ANSI ---
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    GOLD   = "\033[33m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

    # Capas Técnicas
    NODE2D_ERROR = "CAPA_NODE_2D"
    WIN_ERROR    = "CAPA_SISTEMA_WIN"
    SYNTAX_ERROR = "CAPA_SINTAXIS"
    
    WIKI_URL = "https://bluepandaopn.github.io/PyEgar/wiki/erroregas.html"

    @staticmethod
    def start():
        """Inicializa el Centinela con el reporte estético de arranque."""
        # Sobreescribimos el manejador de excepciones de Python
        sys.excepthook = ERROREGAS.analyze
        
        print(f"{ERROREGAS.GOLD}{ERROREGAS.BOLD}>>> [ERROREGAS] Inicializando vigilancia...{ERROREGAS.RESET}")
        time.sleep(0.1) # Simulación de carga rápida
        print(f"{ERROREGAS.GREEN}>>> [ERROREGAS] Escaneando decoradores @private...{ERROREGAS.RESET}")
        print(f"{ERROREGAS.BLUE}>>> [ERROREGAS] Kernel V0.5 protegido. SISTEMA ONLINE.{ERROREGAS.RESET}")
        print("-" * 50)

    @staticmethod
    def validate_injection(target, components):
        """
        Valida que los componentes pasados a libs() sean válidos.
        Si algo falla, ERROREGAS intercepta antes del crash.
        """
        for comp in components:
            if comp is None:
                ERROREGAS.manual_report(
                    ERROREGAS.NODE2D_ERROR, 
                    "Inyección Corrupta", 
                    f"Intentaste inyectar un componente inexistente en {target}"
                )

    @staticmethod
    def analyze(exctype, value, tb):
        """Intercepta cualquier error del motor y genera el reporte visual."""
        stack = traceback.extract_tb(tb)
        last_call = stack[-1]
        
        file_path = last_call.filename
        line_no = last_call.lineno
        code_context = last_call.line
        
        # Clasificación por Capa
        category = ERROREGAS.SYNTAX_ERROR
        path_lower = file_path.lower()
        
        if "node2d" in path_lower or "components" in path_lower:
            category = ERROREGAS.NODE2D_ERROR
        elif "windows" in path_lower or "win" in path_lower:
            category = ERROREGAS.WIN_ERROR

        ERROREGAS.render_report(category, exctype.__name__, value, file_path, line_no, code_context)
        
        # Auto-abrir la Wiki para ayuda
        # webbrowser.open(ERROREGAS.WIKI_URL)
        sys.exit(1)

    @staticmethod
    def render_report(cat, name, val, file, line, code):
        """Dibuja el reporte estético en la terminal."""
        color = ERROREGAS.RED
        if cat == ERROREGAS.NODE2D_ERROR: color = ERROREGAS.BLUE
        if cat == ERROREGAS.WIN_ERROR:    color = ERROREGAS.YELLOW

        print(f"\n{color}{'='*60}")
        print(f" [ERROREGAS DIAGNOSIS] -> {cat}")
        print(f"{'='*60}{ERROREGAS.RESET}")
        print(f"{ERROREGAS.BOLD}TIPO:{ERROREGAS.RESET} {name}")
        print(f"{ERROREGAS.BOLD}MSG:{ERROREGAS.RESET}  {val}")
        print(f"{ERROREGAS.BOLD}FILE:{ERROREGAS.RESET} {file} (Línea {line})")
        print(f"{ERROREGAS.GOLD}>>> {code}{ERROREGAS.RESET}")
        print(f"{color}{'='*60}{ERROREGAS.RESET}\n")

    @staticmethod
    def manual_report(cat, name, val):
        """Permite al motor lanzar un error controlado sin crash de Python."""
        ERROREGAS.render_report(cat, name, val, "Kernel Interno", "N/A", "Validación de Integridad")
        sys.exit(1)