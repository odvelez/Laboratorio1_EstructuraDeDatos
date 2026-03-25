"""
Demo verificable de recovery del indice.

Flujo:
1. Crear datos reales en data.log/index.bin.
2. Borrar index.bin manualmente desde el script.
3. Reinstanciar PersistenceSystem.
4. Verificar que las lecturas siguen funcionando tras reconstruir el indice.
"""

import os
import shutil
import sys
import stat

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.join(PROJECT_ROOT, "game")
sys.path.insert(0, GAME_DIR)

from persistence_system import PersistenceSystem

DEMO_DIR = os.path.join(PROJECT_ROOT, "recovery_demo_data")


def _print_rows(rows):
    for key, value in rows:
        print(f"  - {key}: {value}")


def _remove_readonly(func, path, _exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    if os.path.isdir(DEMO_DIR):
        shutil.rmtree(DEMO_DIR, onerror=_remove_readonly)

    print("=== RECOVERY DEMO ===")
    print(f"Directorio demo: {DEMO_DIR}")

    persistence = PersistenceSystem(DEMO_DIR)
    persistence.clear_all_data()

    samples = [
        ("profile:demo_alice", [1200, [[1200, "2026-03-14", "facil"]], [[1200], [], []], "hash_a", ["facil", 5, 0]]),
        ("profile:demo_bob", [980, [[980, "2026-03-14", "medio"]], [[], [980], []], "hash_b", ["medio", 7, 0]]),
        ("settings:demo_alice", ["facil", 8, 1]),
    ]

    print("\n1) Guardando registros en data.log e index.bin")
    for key, payload in samples:
        saved = persistence.save(key, payload, "demo")
        print(f"  - save({key}) -> {saved}")

    print("\n2) Lecturas antes de borrar index.bin")
    before_rows = []
    for key, _payload in samples:
        before_rows.append((key, persistence.get(key)))
    _print_rows(before_rows)

    print("\n3) Borrando index.bin")
    if os.path.exists(persistence.index_file):
        os.remove(persistence.index_file)
        print(f"  - eliminado: {persistence.index_file}")
    else:
        print("  - index.bin no existia")

    print("\n4) Reinstanciando PersistenceSystem")
    rebuilt_persistence = PersistenceSystem(DEMO_DIR)

    print("\n5) Lecturas despues de reconstruir indice desde data.log")
    after_rows = []
    for key, _payload in samples:
        after_rows.append((key, rebuilt_persistence.get(key)))
    _print_rows(after_rows)

    success = True
    for index in range(len(samples)):
        expected_key = samples[index][0]
        expected_payload = samples[index][1]
        actual_key = after_rows[index][0]
        actual_payload = after_rows[index][1]
        if expected_key != actual_key or expected_payload != actual_payload:
            success = False
            break

    print("\n6) Resultado final")
    print(f"  - recovery_ok: {success}")
    print(f"  - data.log existe: {os.path.exists(rebuilt_persistence.data_file)}")
    print(f"  - index.bin existe: {os.path.exists(rebuilt_persistence.index_file)}")
    print(f"  - claves reconstruidas: {rebuilt_persistence.get_all_keys()}")

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
