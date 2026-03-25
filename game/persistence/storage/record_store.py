import os

from persistence.storage.serializer import Serializer


class RecordStore:
    """Maneja el append-only log `data.log`."""

    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_parent_dir()
        self._ensure_file()

    def _ensure_parent_dir(self):
        parent = os.path.dirname(self.file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "a", encoding="utf-8"):
                pass

    def append_record(self, record_type, key, data):
        self._ensure_file()
        line = Serializer.record_to_line(record_type, key, data, deleted=False)

        with open(self.file_path, "a", encoding="utf-8") as handle:
            offset = handle.tell()
            handle.write(line)

        return offset

    def append_delete_record(self, key):
        self._ensure_file()
        line = Serializer.record_to_line("deleted", key, None, deleted=True)

        with open(self.file_path, "a", encoding="utf-8") as handle:
            offset = handle.tell()
            handle.write(line)

        return offset

    def read_record_at(self, offset):
        if offset is None or not os.path.exists(self.file_path):
            return None

        with open(self.file_path, "r", encoding="utf-8") as handle:
            handle.seek(offset)
            return Serializer.line_to_record(handle.readline())

    def iter_records(self):
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as handle:
            while True:
                offset = handle.tell()
                line = handle.readline()
                if not line:
                    break

                record = Serializer.line_to_record(line)
                if record is not None:
                    yield (offset, record)

    def clear_file(self):
        self._ensure_parent_dir()
        with open(self.file_path, "w", encoding="utf-8"):
            pass
