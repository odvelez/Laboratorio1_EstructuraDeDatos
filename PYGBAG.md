# Ejecutar el juego en el navegador (pygbag)

Este proyecto usa **[pygbag](https://pypi.org/project/pygbag/)** para compilar Python + **pygame-ce** a WebAssembly y probarlo en el navegador.

## Requisitos

- Python 3.8+
- Navegador moderno (Chrome/Edge recomendado para pruebas)

## Instalación

Desde la raíz del repositorio:

```bash
pip install -r requirements-pygbag.txt
```

O manualmente:

```bash
pip install pygame-ce pygbag --upgrade
```

> **Nota:** pygbag está pensado para **pygame-ce**. Si tenías solo `pygame` instalado, desinstálalo o usa un entorno virtual solo para web.

## Cómo lanzar el servidor de prueba (localhost)

El punto de entrada es `game/main.py`. Debes ejecutar **pygbag** apuntando a la carpeta **`game`** (donde está `main.py`):

```bash
cd game
pygbag .
```

O desde la raíz del proyecto:

```bash
pygbag game
```

Abre en el navegador la URL que muestre la consola (por defecto suele ser **http://127.0.0.1:8000**).

## Primera carga

La primera vez puede tardar: pygbag descarga caché de runtime WASM. Si algo falla, borra la carpeta `build` dentro de `game` y vuelve a ejecutar `pygbag`.

## Publicar en la web (GitHub Pages, itch.io, etc.)

Tras `pygbag`, se genera contenido en `game/build/` (o similar). Para un ZIP listo para itch.io:

```bash
cd game
pygbag . --archive
```

Consulta `pygbag --help` para opciones (`--title`, `--icon`, `--html`, etc.).

## Guardado de datos (mismo formato que en consola)

Los datos se escriben en **`game/savegame.json`** con la misma estructura JSON que al ejecutar en escritorio (`crud/save_system.py`). Tras cada guardado se intenta sincronizar el sistema de archivos virtual del navegador (Emscripten) para que no se pierdan datos al cerrar la pestaña.

Si notas que no persiste: no borres datos del sitio para `localhost`, prueba otro navegador o revisa la consola (F12).

## Limitaciones en el navegador

- Pantalla completa (F11) y algunas APIs pueden diferir del escritorio.
- La escena **Hash table** usa dibujo ligero para no congelar el hilo en WASM.

## Ejecución en escritorio (sin navegador)

Sigue funcionando con Python normal:

```bash
cd game
python main.py
```

Con `pygame` o `pygame-ce` instalado (`import pygame` es compatible con ambos en la mayoría de casos).
