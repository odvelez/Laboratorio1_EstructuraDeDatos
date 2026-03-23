"""
Experimentos de Rendimiento - Pruebas de rendimiento del sistema de persistencia

Realiza pruebas de inserción, búsqueda y mide colisiones para diferentes
cantidades de registros: 1000, 5000, 20000.
"""

import time
import random
import string
import sys
import os

# Agregar el directorio game al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

from persistence_system import PersistenceSystem


def generate_random_string(length: int = 10) -> str:
    """Genera una cadena aleatoria."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_test_data(count: int) -> list:
    """Genera datos de prueba."""
    data = []
    for i in range(count):
        username = f"user_{i}"
        profile_data = {
            "maxScore": random.randint(0, 10000),
            "attempts": [
                {
                    "score": random.randint(0, 10000),
                    "fecha": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    "dificultad": random.choice(["facil", "medio", "dificil"])
                }
                for _ in range(random.randint(1, 10))
            ],
            "rankings": {
                "facil": [random.randint(0, 5000) for _ in range(random.randint(1, 5))],
                "medio": [random.randint(0, 8000) for _ in range(random.randint(1, 5))],
                "dificil": [random.randint(0, 10000) for _ in range(random.randint(1, 5))]
            },
            "password": generate_random_string(16)
        }
        data.append((username, profile_data))
    return data


def run_performance_test(record_count: int) -> dict:
    """
    Ejecuta pruebas de rendimiento para una cantidad específica de registros.

    Args:
        record_count: Número de registros a probar

    Returns:
        Diccionario con resultados de las pruebas
    """
    print(f"\n=== Prueba de Rendimiento: {record_count} registros ===")

    # Limpiar datos anteriores
    persistence = PersistenceSystem(".")
    persistence.clear_all_data()

    # Generar datos de prueba
    test_data = generate_test_data(record_count)
    print(f"Datos de prueba generados: {len(test_data)} registros")

    # Prueba de inserción
    print("Midiendo tiempo de inserción...")
    start_time = time.time()

    for username, profile_data in test_data:
        key = f"profile:{username}"
        persistence.save(key, profile_data, "profile")

    insert_time = time.time() - start_time
    print(".2f")

    # Obtener estadísticas después de inserción
    stats_after_insert = persistence.get_stats()
    print(f"Estadísticas después de inserción: {stats_after_insert}")

    # Prueba de búsqueda
    print("Midiendo tiempo de búsqueda...")
    search_keys = [f"profile:user_{random.randint(0, record_count-1)}" for _ in range(min(1000, record_count))]

    start_time = time.time()
    found_count = 0

    for key in search_keys:
        if persistence.get(key) is not None:
            found_count += 1

    search_time = time.time() - start_time
    search_avg_time = search_time / len(search_keys)
    print(".2f")
    print(f"Registros encontrados: {found_count}/{len(search_keys)}")

    # Calcular colisiones (estimación basada en la estructura de la tabla)
    # Para una estimación simple, podemos usar la información de la tabla hash
    ht = persistence.index
    total_buckets = ht.size
    occupied_buckets = sum(1 for i in range(ht.size) if ht.table[i] is not None)
    total_entries = ht.count

    # Calcular distribución de colisiones
    chain_lengths = []
    for i in range(ht.size):
        length = 0
        entry = ht.table[i]
        while entry is not None:
            length += 1
            entry = entry.next
        if length > 0:
            chain_lengths.append(length)

    avg_chain_length = sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0
    max_chain_length = max(chain_lengths) if chain_lengths else 0

    # Calcular factor de carga
    load_factor = ht.load_factor

    results = {
        "record_count": record_count,
        "insert_time": insert_time,
        "search_time": search_time,
        "search_avg_time": search_avg_time,
        "found_count": found_count,
        "total_searches": len(search_keys),
        "stats_after_insert": stats_after_insert,
        "total_buckets": total_buckets,
        "occupied_buckets": occupied_buckets,
        "total_entries": total_entries,
        "load_factor": load_factor,
        "avg_chain_length": avg_chain_length,
        "max_chain_length": max_chain_length,
        "collision_info": {
            "chains_with_length_1": sum(1 for l in chain_lengths if l == 1),
            "chains_with_length_2": sum(1 for l in chain_lengths if l == 2),
            "chains_with_length_3_plus": sum(1 for l in chain_lengths if l >= 3),
        }
    }

    return results


def run_all_tests():
    """Ejecuta todas las pruebas de rendimiento."""
    test_sizes = [1000, 5000, 20000]
    all_results = []

    print("=== EXPERIMENTOS DE RENDIMIENTO ===")
    print("Sistema de Persistencia basado en Tabla Hash")
    print("=" * 50)

    for size in test_sizes:
        try:
            results = run_performance_test(size)
            all_results.append(results)
        except Exception as e:
            print(f"Error en prueba de {size} registros: {e}")
            continue

    # Resumen final
    print("\n" + "=" * 50)
    print("RESUMEN DE RESULTADOS")
    print("=" * 50)

    print("<10")
    print("-" * 70)
    print("<10")
    print("-" * 70)

    for result in all_results:
        count = result["record_count"]
        insert_time = result["insert_time"]
        search_time = result["search_time"]
        load_factor = result["load_factor"]
        avg_chain = result["avg_chain_length"]
        max_chain = result["max_chain_length"]

        print("<10")

    print("\nPruebas completadas. Los archivos data.log e index.bin contienen los datos de prueba.")


if __name__ == "__main__":
    run_all_tests()</content>
<parameter name="filePath">c:\Users\isaac\OneDrive\Documents\UNINORTE\III SEMESTRE\Estructura de datos\Laboratorio1_EstructuraDeDatos\performance_tests.py