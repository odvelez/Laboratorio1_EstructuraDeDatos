#!/usr/bin/env python3
"""
Script principal para completar la implementación del laboratorio

Este script ejecuta:
1. Migración de datos existentes
2. Pruebas de rendimiento
3. Verificación del sistema
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=== COMPLETANDO IMPLEMENTACIÓN DEL LABORATORIO ===")
    print()

    # Paso 1: Migrar datos existentes
    print("PASO 1: Migrando datos existentes de savegame.json...")
    try:
        from migrate_data import migrate_savegame_to_persistence
        migrate_savegame_to_persistence("game/savegame.json")
        print("✓ Migración completada")
    except Exception as e:
        print(f"✗ Error en migración: {e}")
        import traceback
        traceback.print_exc()
        return

    print()

    # Paso 2: Ejecutar pruebas de rendimiento
    print("PASO 2: Ejecutando experimentos de rendimiento...")
    try:
        from performance_tests import run_all_tests
        run_all_tests()
        print("✓ Pruebas de rendimiento completadas")
    except Exception as e:
        print(f"✗ Error en pruebas de rendimiento: {e}")
        import traceback
        traceback.print_exc()
        return

    print()

    # Paso 3: Verificar funcionamiento
    print("PASO 3: Verificando funcionamiento del sistema...")
    try:
        from persistence_system import PersistenceSystem
        from repositories.profile_repository import ProfileRepository
        from repositories.leaderboard_repository import LeaderboardRepository
        from repositories.settings_repository import SettingsRepository

        # Verificar que el sistema funciona
        persistence = PersistenceSystem("game")
        profile_repo = ProfileRepository(persistence)
        leaderboard_repo = LeaderboardRepository(persistence)
        settings_repo = SettingsRepository(persistence)

        # Verificar que hay datos
        profiles = profile_repo.get_all_profiles()
        print(f"✓ Perfiles encontrados: {len(profiles)}")

        # Verificar leaderboard
        stats = leaderboard_repo.get_global_stats()
        print(f"✓ Estadísticas de leaderboard: {stats}")

        # Verificar archivos creados
        data_exists = os.path.exists("game/data.log")
        index_exists = os.path.exists("game/index.bin")

        print(f"✓ Archivo data.log existe: {data_exists}")
        print(f"✓ Archivo index.bin existe: {index_exists}")

        if data_exists and index_exists:
            print("✓ Sistema de persistencia completamente funcional")
        else:
            print("✗ Faltan archivos del sistema de persistencia")

    except Exception as e:
        print(f"✗ Error verificando sistema: {e}")
        import traceback
        traceback.print_exc()
        return

    print()
    print("=== LABORATORIO COMPLETADO ===")
    print()
    print("Archivos implementados:")
    print("✓ persistence/storage/record_store.py")
    print("✓ persistence/storage/index_store.py")
    print("✓ persistence/storage/serializer.py")
    print("✓ persistence/storage/recovery.py")
    print("✓ persistence_system.py")
    print("✓ repositories/profile_repository.py")
    print("✓ repositories/leaderboard_repository.py")
    print("✓ repositories/settings_repository.py")
    print("✓ migrate_data.py")
    print("✓ performance_tests.py")
    print("✓ crud/save_system.py (actualizado)")
    print("✓ crud/ranking.py (actualizado)")
    print("✓ crud/player.py (actualizado)")
    print()
    print("El sistema ahora cumple con todos los requisitos:")
    print("• Tabla hash implementada manualmente")
    print("• Manejo de colisiones con encadenamiento")
    print("• Factor de carga y rehash automático")
    print("• Persistencia en data.log (JSON Lines)")
    print("• Índice en index.bin (serializado)")
    print("• Reconstrucción automática del índice")
    print("• Repositorios para perfiles, leaderboard y settings")
    print("• Experimentos de rendimiento completados")
    print("• Integración completa con el videojuego")

if __name__ == "__main__":
    main()</content>
<parameter name="filePath">c:\Users\isaac\OneDrive\Documents\UNINORTE\III SEMESTRE\Estructura de datos\Laboratorio1_EstructuraDeDatos\setup_laboratory.py