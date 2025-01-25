import os
import sys
from pathlib import Path

# Obtener el directorio raíz del proyecto
root_dir = Path(__file__).parent.parent

# Agregar src al PYTHONPATH
sys.path.insert(0, str(root_dir / 'src')) 