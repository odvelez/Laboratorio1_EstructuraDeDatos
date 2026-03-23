"""
Profile Repository - Gestión de perfiles de usuario

Usa el sistema de persistencia para guardar/cargar perfiles.
"""

from typing import Optional, Dict, Any
from persistence_system import PersistenceSystem


class ProfileRepository:
    """Repositorio para perfiles de usuario."""

    def __init__(self, persistence_system: PersistenceSystem):
        self.persistence = persistence_system

    def save_profile(self, username: str, profile_data: Dict[str, Any]) -> bool:
        key = f"profile:{username}"
        return self.persistence.save(key, profile_data, "profile")

    def get_profile(self, username: str) -> Optional[Dict[str, Any]]:
        key = f"profile:{username}"
        return self.persistence.get(key)

    def delete_profile(self, username: str) -> bool:
        key = f"profile:{username}"
        return self.persistence.delete(key)

    def profile_exists(self, username: str) -> bool:
        key = f"profile:{username}"
        return self.persistence.contains(key)

    def get_all_profiles(self) -> Dict[str, Dict[str, Any]]:
        profiles = {}
        for key in self.persistence.get_all_keys():
            if key.startswith("profile:"):
                username = key[8:]
                profile = self.persistence.get(key)
                if profile:
                    profiles[username] = profile
        return profiles
