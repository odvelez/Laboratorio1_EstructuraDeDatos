"""
Migración de datos - Migra savegame.json al nuevo sistema de persistencia

Este script migra los datos existentes del archivo JSON al sistema
de persistencia basado en archivos.
"""

import json
import os
import sys

# Agregar el directorio game al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game'))

from persistence_system import PersistenceSystem
from repositories.profile_repository import ProfileRepository
from repositories.leaderboard_repository import LeaderboardRepository
from repositories.settings_repository import SettingsRepository


def migrate_savegame_to_persistence(savegame_file: str = "savegame.json"):
    """
    Migra los datos de savegame.json al nuevo sistema de persistencia.

    Args:
        savegame_file: Ruta al archivo savegame.json
    """
    if not os.path.exists(savegame_file):
        print(f"Archivo {savegame_file} no encontrado. Nada que migrar.")
        return

    # Cargar datos existentes
    with open(savegame_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Inicializar sistema de persistencia
    persistence = PersistenceSystem(".")

    # Inicializar repositorios
    profile_repo = ProfileRepository(persistence)
    leaderboard_repo = LeaderboardRepository(persistence)
    settings_repo = SettingsRepository(persistence)

    players = data.get("players", {})

    print(f"Migrando {len(players)} perfiles de usuario...")

    for username, player_data in players.items():
        print(f"Migrando perfil de {username}...")

        # Extraer datos del perfil
        profile_data = {
            "maxScore": player_data.get("maxScore", 0),
            "attempts": player_data.get("attempts", []),
            "rankings": player_data.get("rankings", {}),
            "password": player_data.get("password", ""),
        }

        # Guardar perfil
        profile_repo.save_profile(username, profile_data)

        # Extraer y guardar configuraciones
        settings = player_data.get("settings", {})
        if settings:
            settings_repo.save_settings(username, settings)

        # Extraer y guardar puntajes individuales
        attempts = player_data.get("attempts", [])
        for attempt in attempts:
            if isinstance(attempt, dict):
                score = attempt.get("score", 0)
                timestamp = attempt.get("fecha", "")
                difficulty = attempt.get("dificultad", "medio")

                leaderboard_repo.save_score(username, score, difficulty, timestamp)

    print("Migración completada.")
    print(f"Estadísticas del sistema: {persistence.get_stats()}")


if __name__ == "__main__":
    migrate_savegame_to_persistence()</content>
<parameter name="filePath">c:\Users\isaac\OneDrive\Documents\UNINORTE\III SEMESTRE\Estructura de datos\Laboratorio1_EstructuraDeDatos\migrate_data.py