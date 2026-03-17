from persistence.hash_entry import HashEntry


class HashTable:
    def __init__(self, size=64):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash(self, key):
        """Función hash manual usando multiplicación polinómica."""
        h = 0
        for char in str(key):
            h = (h * 31 + ord(char)) & 0xFFFFFFFF
        return h % self.size

    def put(self, key, value):
        index = self._hash(key)
        entry = self.table[index]

        while entry is not None:
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next

        new_entry = HashEntry(key, value)
        new_entry.next = self.table[index]
        self.table[index] = new_entry
        self.count += 1

    def get(self, key):
        index = self._hash(key)
        entry = self.table[index]

        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next

        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        index = self._hash(key)
        entry = self.table[index]
        prev = None

        while entry is not None:
            if entry.key == key:
                if prev is None:
                    self.table[index] = entry.next
                else:
                    prev.next = entry.next
                self.count -= 1
                return True
            prev = entry
            entry = entry.next

        return False

    def keys(self):
        result = []
        for bucket in self.table:
            entry = bucket
            while entry is not None:
                result.append(entry.key)
                entry = entry.next
        return result

    def values(self):
        result = []
        for bucket in self.table:
            entry = bucket
            while entry is not None:
                result.append(entry.value)
                entry = entry.next
        return result

    def items(self):
        result = []
        for bucket in self.table:
            entry = bucket
            while entry is not None:
                result.append((entry.key, entry.value))
                entry = entry.next
        return result

    def __len__(self):
        return self.count


def hash_string(text):
    """Función hash manual para convertir texto en un valor numérico hexadecimal.
    Usada para hashear contraseñas sin librerías externas."""
    h1 = 0x811C9DC5
    h2 = 0x01000193

    for char in text:
        code = ord(char)
        h1 = ((h1 ^ code) * 0x01000193) & 0xFFFFFFFF
        h2 = ((h2 * 31) + code + h1) & 0xFFFFFFFF

    combined = ((h1 << 32) | h2) & 0xFFFFFFFFFFFFFFFF
    return format(combined, "016x")
