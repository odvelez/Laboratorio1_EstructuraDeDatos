import json
import os

SAVE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "savegame.json")

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
    # Mismo JSON que en consola; en navegador (WASM) intentar persistir FS → IndexedDB
    _try_sync_browser_filesystem()


def _try_sync_browser_filesystem():
    """En Emscripten/pygbag, volcar el FS virtual al almacenamiento del navegador."""
    try:
        import sys

        if getattr(sys, "platform", "") != "emscripten":
            return
        # Pyodide expone FS.syncfs en algunos entornos pygame-web
        try:
            from pyodide_js._module import FS  # type: ignore

            FS.syncfs(False, lambda err: None)
        except Exception:
            try:
                import pyodide_js  # type: ignore

                if hasattr(pyodide_js, "fs") and hasattr(pyodide_js.fs, "syncfs"):
                    pyodide_js.fs.syncfs(False, lambda err: None)
            except Exception:
                pass
    except Exception:
        pass


def _copiar_estructura():
    return json.loads(json.dumps(_ESTRUCTURA_BASE))
