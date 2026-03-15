# utils.py
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta para archivos incluidos en el exe."""
    try:
        # Si se ejecuta desde el EXE
        base_path = sys._MEIPASS
    except Exception:
        # Si se ejecuta desde Python normal
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)