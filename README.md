# Laboratorio 1 - Persistencia con tabla hash en archivos

Proyecto academico: videojuego en **Pygame** con capa de persistencia basada en **tabla hash manual**, archivos **`data.log`** (JSON Lines) e **`index.bin`** (indice serializado), cumpliendo las restricciones del laboratorio en la capa de persistencia (sin `dict` / `set` nativos para el nucleo indexado).

## Arquitectura

| Componente | Rol |
|--------------|-----|
| `game/persistence/hash_table.py`, `hash_entry.py` | Tabla hash con **encadenamiento**, factor de carga y **rehash** |
| `game/persistence/storage/record_store.py` | Append-only en `data.log` |
| `game/persistence/storage/index_store.py` | Serializacion del indice en `index.bin` |
| `game/persistence/storage/serializer.py` | Conversion registro / linea JSON |
| `game/persistence/storage/recovery.py` | Reconstruccion del indice desde el log |
| `game/persistence_system.py` | API: `save`, `get`, `delete`, `rebuild_index` |
| `game/repositories/*.py` | Perfiles, leaderboard y ajustes sobre el sistema anterior |
| `game/scenes/` | Login, menu, runner, leaderboard, settings, visualizacion hash |

Los datos de juego suelen residir en la carpeta **`game/`** (`data.log`, `index.bin`). Puede existir **`game/savegame.json`** como respaldo o migracion desde versiones anteriores.

## Requisitos

- Python 3.8+
- `pygame` o `pygame-ce`

```bash
pip install pygame
# o: pip install pygame-ce
```

## Ejecutar el juego (escritorio)

```bash
cd game
python main.py
```

## Pygbag (navegador)

Instalacion y detalles: **[PYGBAG.md](PYGBAG.md)**.

```bash
pip install -r requirements-pygbag.txt
cd game
pygbag .
```

Tras operaciones de guardado, el backend intenta sincronizar el sistema de archivos del navegador (cuando aplica) para persistir `data.log` / `index.bin` en el entorno web.

## Migracion desde JSON (opcional)

Si teneis datos antiguos en `savegame.json`:

```bash
# Desde la raiz del repo; si el archivo esta en game/, ajusta la ruta en migrate_data.py o el cwd
python migrate_data.py
```

## Pruebas de rendimiento

Desde la raiz del repositorio:

```bash
python performance_tests.py
```

Incluye cargas de **1000, 5000 y 20000** registros e informa tiempos de insercion/busqueda, colisiones y factor de carga (valores concretos dependen de la maquina).

## Demo de recuperacion del indice

Demuestra borrar **`index.bin`**, reconstruir desde **`data.log`** y comprobar lecturas:

```bash
python recovery_demo.py
```

Usa la carpeta `recovery_demo_data/` (se puede regenerar al ejecutar el script).

## Checklist de cumplimiento (resumen)

- Tabla hash manual con encadenamiento y rehash por factor de carga
- Persistencia `data.log` + `index.bin`
- Reconstruccion del indice desde el log
- Integracion con el videojuego (escenas y repositorios)
- Pruebas de rendimiento y demo de recovery
- Ejecucion en escritorio y con **pygbag** (ver **PYGBAG.md**)

## Estructura de carpetas (resumen)

```text
Laboratorio1_Estructura/
├── game/
│   ├── main.py
│   ├── persistence_system.py
│   ├── persistence/
│   ├── repositories/
│   ├── scenes/
│   └── ...
├── performance_tests.py
├── recovery_demo.py
├── migrate_data.py
├── README.md
└── PYGBAG.md
```

---

Guarda este archivo siempre como **UTF-8** (sin BOM) para evitar corrupcion al abrirlo en otros editores o tras sincronizar con la nube.
