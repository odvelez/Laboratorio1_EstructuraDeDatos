import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "savegame.json")

game_state = {
    "puntaje": 0,
    "distancia": 0,
    "dificultad": "medio",
    "velocidad_juego": 6,
    "nivel": 1,
}


def guardar_progreso():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(game_state, f, indent=4, ensure_ascii=False)


def cargar_progreso():
    if not os.path.exists(SAVE_FILE):
        return

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return

    if not isinstance(datos, dict):
        return

    for clave in game_state:
        if clave in datos:
            game_state[clave] = datos[clave]
