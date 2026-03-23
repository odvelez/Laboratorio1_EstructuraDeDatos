# Laboratorio 1 - Persistencia de Videojuegos con Tabla Hash

## Descripción

Este proyecto implementa un sistema completo de persistencia para videojuegos basado en una tabla hash implementada desde cero. El sistema cumple con todos los requisitos del laboratorio de Estructuras de Datos.

## Arquitectura del Sistema

### Componentes Principales

1. **Tabla Hash Manual** (`persistence/hash_table.py`)
   - Implementada desde cero sin usar `dict`, `set` u otras estructuras nativas
   - Encadenamiento separado para manejo de colisiones
   - Factor de carga automático con rehash cuando supera 0.75

2. **Sistema de Persistencia** (`persistence_system.py`)
   - API unificada para operaciones de persistencia
   - Integración de todos los componentes de storage

3. **Storage Layer**
   - `record_store.py`: Maneja `data.log` (formato JSON Lines)
   - `index_store.py`: Serializa tabla hash a `index.bin`
   - `serializer.py`: Utilidades de serialización
   - `recovery.py`: Reconstrucción automática del índice

4. **Repositories**
   - `profile_repository.py`: Gestión de perfiles de usuario
   - `leaderboard_repository.py`: Gestión de rankings y puntajes
   - `settings_repository.py`: Gestión de configuraciones

## Formato de Archivos

### data.log (JSON Lines)
```json
{"type":"profile","key":"player:1","data":{"level":5,"coins":200}}
{"type":"score","key":"run:12","data":{"score":3200}}
{"type":"settings","key":"settings:1","data":{"volume":80,"difficulty":"normal"}}
```

### index.bin
Archivo binario que contiene la tabla hash serializada con referencias a posiciones en data.log.

## Videojuego

El proyecto incluye un videojuego completo (endless runner) con:

- **Pantallas**: Login, Menú, Juego, Leaderboard, Configuraciones, Visualización de Tabla Hash
- **Persistencia**: Perfiles, puntajes, configuraciones
- **Web**: Compatible con Pygbag para ejecución en navegador

## Instalación y Uso

### Requisitos
- Python 3.8+
- Pygame y Pygbag para versión web

### Configuración Completa
```bash
# Ejecutar setup completo (migración + pruebas)
python setup_laboratory.py
```

### Uso Individual

#### Migrar datos existentes
```bash
python migrate_data.py
```

#### Ejecutar pruebas de rendimiento
```bash
python performance_tests.py
```

#### Ejecutar el juego
```bash
cd game
python main.py
```

#### Versión web
```bash
cd game
pygbag .
```

## Experimentos de Rendimiento

El sistema incluye pruebas automáticas con:
- **1000 registros**: Medición de tiempo de inserción/búsqueda
- **5000 registros**: Análisis de colisiones y factor de carga
- **20000 registros**: Rendimiento a gran escala

### Resultados Típicos
- Tiempo de inserción: ~0.1-0.5 segundos por 1000 registros
- Factor de carga: Mantenido por debajo de 0.75 con rehash automático
- Colisiones: Distribución uniforme con encadenamiento eficiente

## API de Uso

### Sistema de Persistencia
```python
from persistence_system import PersistenceSystem

# Inicializar
persistence = PersistenceSystem(".")

# Operaciones básicas
persistence.save("user:1", {"name": "John", "score": 100})
data = persistence.get("user:1")
persistence.delete("user:1")
```

### Repositorios
```python
from repositories.profile_repository import ProfileRepository

repo = ProfileRepository(persistence)
repo.save_profile("john", {"maxScore": 1000, "attempts": []})
profile = repo.get_profile("john")
```

## Características Técnicas

- **Colisiones**: Encadenamiento separado (separate chaining)
- **Rehash**: Automático cuando factor de carga > 0.75
- **Recuperación**: Reconstrucción automática del índice desde data.log
- **Serialización**: Pickle para tabla hash, JSON Lines para datos
- **Compresión**: No implementada (datos se almacenan en texto plano)

## Estructura de Archivos

```
Laboratorio1_EstructuraDeDatos/
├── game/
│   ├── main.py                 # Punto de entrada del juego
│   ├── scenes/                 # Pantallas del juego
│   ├── crud/                   # Lógica de negocio
│   ├── persistence/            # Tabla hash y sistema de persistencia
│   │   ├── hash_table.py
│   │   ├── hash_entry.py
│   │   └── storage/
│   │       ├── record_store.py
│   │       ├── index_store.py
│   │       ├── serializer.py
│   │       └── recovery.py
│   ├── persistence_system.py   # API unificada
│   └── savegame.json          # Datos legacy (para compatibilidad)
├── repositories/               # Repositorios de datos
│   ├── profile_repository.py
│   ├── leaderboard_repository.py
│   └── settings_repository.py
├── migrate_data.py            # Migración de datos
├── performance_tests.py       # Experimentos de rendimiento
├── setup_laboratory.py        # Configuración completa
└── README.md
```

## Cumplimiento de Requisitos

✅ **Tabla hash manual** - Sin uso de estructuras nativas
✅ **Manejo de colisiones** - Encadenamiento separado
✅ **Factor de carga** - Rehash automático
✅ **Persistencia** - data.log + index.bin
✅ **Reconstrucción** - Índice se reconstruye desde datos
✅ **Videojuego** - Completo con todas las pantallas
✅ **Web** - Compatible con Pygbag
✅ **Experimentos** - Pruebas con múltiples tamaños de datos

## Licencia

Proyecto educativo para el curso de Estructuras de Datos.