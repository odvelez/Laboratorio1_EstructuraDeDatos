import os

from persistence.storage.serializer import Serializer


class IndexStore:
    """Persistencia del índice serializado en `index.bin`."""

    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_parent_dir()

    def _ensure_parent_dir(self):
        parent = os.path.dirname(self.file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def save_index(self, hash_table):
        self._ensure_parent_dir()
        raw = Serializer.serialize_index(hash_table)

        with open(self.file_path, "wb") as handle:
            handle.write(raw)

        return True

    def load_index(self):
        if not os.path.exists(self.file_path):
            return None

        with open(self.file_path, "rb") as handle:
            return Serializer.deserialize_index(handle.read())

    def delete_index(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
