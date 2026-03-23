"""
Persistence System - Sistema completo de persistencia

Integra record_store, index_store, recovery y serializer
para proporcionar una API unificada de persistencia.
"""

import os
from typing import Dict, Any, Optional
from persistence.hash_table import HashTable
from persistence.storage.record_store import RecordStore
from persistence.storage.index_store import IndexStore
from persistence.storage.recovery import Recovery


class PersistenceSystem:
    """
    Sistema completo de persistencia basado en tabla hash.

    Maneja data.log (registros) e index.bin (índice) automáticamente.
    """

    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, "data.log")
        self.index_file = os.path.join(data_dir, "index.bin")

        self.record_store = RecordStore(self.data_file)
        self.index_store = IndexStore(self.index_file)
        self.recovery = Recovery(self.record_store)

        self.index = self._load_or_rebuild_index()

    def _load_or_rebuild_index(self) -> HashTable:
        """
        Carga el índice si existe y es válido, sino lo reconstruye.

        Returns:
            Tabla hash del índice
        """
        # Intentar cargar índice existente
        ht = self.index_store.load_index()

        if ht is not None and self.recovery.validate_index(ht):
            return ht
        else:
            # Reconstruir índice desde data.log
            print("Reconstruyendo índice desde data.log...")
            ht = self.recovery.rebuild_index()
            self.index_store.save_index(ht)
            return ht

    def save(self, key: str, data: Dict[str, Any], record_type: str = "data") -> bool:
        """
        Guarda datos con una clave específica.

        Args:
            key: Clave única del registro
            data: Datos a guardar
            record_type: Tipo de registro

        Returns:
            True si se guardó correctamente
        """
        try:
            # Agregar registro a data.log
            offset = self.record_store.append_record(record_type, key, data)

            # Actualizar índice
            self.index.put(key, offset)

            # Guardar índice actualizado
            return self.index_store.save_index(self.index)

        except Exception as e:
            print(f"Error guardando datos: {e}")
            return False

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos por clave.

        Args:
            key: Clave del registro

        Returns:
            Datos del registro o None si no existe
        """
        return self.recovery.get_record_data(self.index, key)

    def delete(self, key: str) -> bool:
        """
        Elimina un registro por clave.

        Args:
            key: Clave del registro a eliminar

        Returns:
            True si se eliminó correctamente
        """
        try:
            # Eliminar del índice
            if self.index.delete(key):
                # Guardar índice actualizado
                return self.index_store.save_index(self.index)
            return False

        except Exception as e:
            print(f"Error eliminando datos: {e}")
            return False

    def contains(self, key: str) -> bool:
        """
        Verifica si existe un registro con la clave dada.

        Args:
            key: Clave a verificar

        Returns:
            True si existe
        """
        return self.index.contains(key)

    def get_all_keys(self) -> list:
        """
        Obtiene todas las claves existentes.

        Returns:
            Lista de claves
        """
        return self.index.keys()

    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema de persistencia.

        Returns:
            Diccionario con estadísticas
        """
        return {
            "index_size": self.index.size,
            "index_count": self.index.count,
            "load_factor": self.index.load_factor,
            "data_file_size": os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0,
            "index_file_size": os.path.getsize(self.index_file) if os.path.exists(self.index_file) else 0,
        }

    def rebuild_index(self) -> bool:
        """
        Fuerza la reconstrucción del índice desde data.log.

        Returns:
            True si se reconstruyó correctamente
        """
        try:
            self.index = self.recovery.rebuild_index()
            return self.index_store.save_index(self.index)
        except Exception as e:
            print(f"Error reconstruyendo índice: {e}")
            return False

    def clear_all_data(self):
        """Limpia todos los datos (usar con precaución)."""
        self.record_store.clear_file()
        self.index_store.delete_index()
        self.index = HashTable()
