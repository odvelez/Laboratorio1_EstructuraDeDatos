"""
Singleton del backend de persistencia del laboratorio.

Todas las escenas y módulos del juego importan `get_persistence()` desde aquí
para compartir la misma instancia de PersistenceSystem apuntando a game/.
"""

import os
from persistence_system import PersistenceSystem

_GAME_DIR = os.path.dirname(os.path.abspath(__file__))

_instance = None


def get_persistence():
    """Retorna la instancia única de PersistenceSystem (data_dir = game/)."""
    global _instance
    if _instance is None:
        _instance = PersistenceSystem(_GAME_DIR)
    return _instance
