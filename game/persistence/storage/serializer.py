import json

from persistence.hash_table import HashTable


class Serializer:
    """Serializa registros del log y el índice binario."""

    @staticmethod
    def record_to_line(record_type, key, data, deleted=False):
        payload = [record_type, key, data, 1 if deleted else 0]
        return json.dumps(payload, ensure_ascii=False) + "\n"

    @staticmethod
    def line_to_record(line):
        raw = line.strip()
        if not raw:
            return None

        try:
            payload = json.loads(raw)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None

        if not isinstance(payload, list) and not isinstance(payload, tuple):
            return None
        if len(payload) != 4:
            return None

        record_type = payload[0]
        key = payload[1]
        data = payload[2]
        deleted = bool(payload[3])
        if key is None or record_type is None:
            return None

        return (record_type, key, data, deleted)

    @staticmethod
    def serialize_index(hash_table):
        payload = [hash_table.size, hash_table.items()]
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")

    @staticmethod
    def deserialize_index(raw_bytes):
        if not raw_bytes:
            return HashTable()

        try:
            payload = json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
            return None

        if not isinstance(payload, list) and not isinstance(payload, tuple):
            return None
        if len(payload) != 2:
            return None

        size = payload[0]
        items = payload[1]

        hash_table = HashTable(size)
        if not isinstance(items, list):
            return None

        for item in items:
            if not isinstance(item, list) and not isinstance(item, tuple):
                return None
            if len(item) != 2:
                return None
            hash_table.put(item[0], item[1])

        return hash_table
