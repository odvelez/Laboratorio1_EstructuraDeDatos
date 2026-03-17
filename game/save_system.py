import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "savegame.json")

_ESTRUCTURA_BASE = {"players": {}}


def cargar_datos():
    if not os.path.exists(SAVE_FILE):
        return _copiar_estructura()

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (json.JSONDecodeError, ValueError, OSError):
        return _copiar_estructura()

    if not isinstance(datos, dict) or "players" not in datos:
        return _copiar_estructura()

    return datos


def guardar_datos(datos):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def _copiar_estructura():
    return json.loads(json.dumps(_ESTRUCTURA_BASE))
