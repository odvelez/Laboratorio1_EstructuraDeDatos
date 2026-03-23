from persistence.hash_table import HashTable


class Recovery:
    """Reconstruye y valida el índice usando `data.log`."""

    def __init__(self, record_store):
        self.record_store = record_store

    def rebuild_index(self):
        hash_table = HashTable()

        for offset, record in self.record_store.iter_records():
            record_type, key, _data, deleted = record
            if deleted or record_type == "deleted":
                hash_table.delete(key)
            else:
                hash_table.put(key, offset)

        return hash_table

    def get_record_data(self, index, key):
        offset = index.get(key)
        if offset is None:
            return None

        record = self.record_store.read_record_at(offset)
        if record is None:
            return None

        record_type, record_key, data, deleted = record
        if deleted or record_type == "deleted" or record_key != key:
            return None

        return data

    def validate_index(self, hash_table):
        for key, offset in hash_table.items():
            record = self.record_store.read_record_at(offset)
            if record is None:
                return False

            record_type, record_key, _data, deleted = record
            if deleted or record_type == "deleted":
                return False
            if record_key != key:
                return False

        return True
