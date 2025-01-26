import os
import sys
from pathlib import Path

# Obtener el directorio raíz del proyecto
root_dir = Path(__file__).parent.parent

# Agregar src y layer al PYTHONPATH
sys.path.insert(0, str(root_dir / 'src'))
sys.path.insert(0, str(root_dir / 'src/layers/common/python'))

# Fixtures comunes
import pytest

@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Configura variables de ambiente para todas las pruebas"""
    monkeypatch.setenv('AWS_SAM_LOCAL', 'true')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG') 