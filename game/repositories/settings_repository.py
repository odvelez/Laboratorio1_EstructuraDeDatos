"""
Settings Repository - Gestión de configuraciones

Usa el sistema de persistencia para guardar/cargar configuraciones.
"""

from typing import Dict, Any, Optional
from persistence_system import PersistenceSystem


class SettingsRepository:
    """Repositorio para configuraciones del juego."""

    def __init__(self, persistence_system: PersistenceSystem):
        self.persistence = persistence_system

    def save_settings(self, username: str, settings: Dict[str, Any]) -> bool:
        key = f"settings:{username}"
        return self.persistence.save(key, settings, "settings")

    def get_settings(self, username: str) -> Optional[Dict[str, Any]]:
        key = f"settings:{username}"
        return self.persistence.get(key)

    def update_setting(self, username: str, setting_key: str, value: Any) -> bool:
        settings = self.get_settings(username) or {}
        settings[setting_key] = value
        return self.save_settings(username, settings)

    def get_default_settings(self) -> Dict[str, Any]:
        return {
            "difficulty": "medio",
            "volume": 5,
            "fullscreen": False,
            "sound_enabled": True,
            "music_enabled": True
        }

    def get_settings_with_defaults(self, username: str) -> Dict[str, Any]:
        user_settings = self.get_settings(username) or {}
        defaults = self.get_default_settings()
        result = defaults.copy()
        result.update(user_settings)
        return result

    def delete_settings(self, username: str) -> bool:
        key = f"settings:{username}"
        return self.persistence.delete(key)

    def settings_exist(self, username: str) -> bool:
        key = f"settings:{username}"
        return self.persistence.contains(key)
