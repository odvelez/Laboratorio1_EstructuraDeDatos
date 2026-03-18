from persistence.hash_entry import HashEntry


class HashTable:
    LOAD_FACTOR_GROW   = 0.75  # rehash x2  cuando count/size >= 0.75
    LOAD_FACTOR_SHRINK = 0.25  # rehash /2  cuando count/size <= 0.25
    MIN_SIZE           = 16    # tamaño mínimo permitido

    def __init__(self, size=64):
        self.size  = max(size, self.MIN_SIZE)
        self.table = [None] * self.size
        self.count = 0

    # ── Factor de carga ───────────────────────
    @property
    def load_factor(self):
        return self.count / self.size

    # ── Hash interno ──────────────────────────
    def _hash(self, key):
        """Función hash manual usando multiplicación polinómica."""
        h = 0
        for char in str(key):
            h = (h * 31 + ord(char)) & 0xFFFFFFFF
        return h % self.size

    # ── Rehash (reconstrucción del índice) ────
    def _rehash(self, new_size):
        """Reconstruye la tabla con nuevo tamaño y recalcula todos los índices."""
        new_size   = max(new_size, self.MIN_SIZE)
        old_items  = self.items()       # guarda todos los pares actuales

        self.size  = new_size
        self.table = [None] * self.size
        self.count = 0

        for key, value in old_items:   # re-inserta recalculando índices
            self._insert(key, value)

    # ── Inserción interna (sin verificar factor de carga) ─
    def _insert(self, key, value):
        index = self._hash(key)
        entry = self.table[index]

        while entry is not None:
            if entry.key == key:       # actualizar existente
                entry.value = value
                return
            entry = entry.next

        new_entry       = HashEntry(key, value)
        new_entry.next  = self.table[index]
        self.table[index] = new_entry
        self.count += 1

    # ── put (público) ─────────────────────────
    def put(self, key, value):
        self._insert(key, value)

        # crecer si se supera el umbral
        if self.load_factor >= self.LOAD_FACTOR_GROW:
            self._rehash(self.size * 2)

    # ── get ───────────────────────────────────
    def get(self, key):
        index = self._hash(key)
        entry = self.table[index]

        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next

        return None

    # ── contains ─────────────────────────────
    def contains(self, key):
        return self.get(key) is not None

    # ── remove ───────────────────────────────
    def remove(self, key):
        index = self._hash(key)
        entry = self.table[index]
        prev  = None

        while entry is not None:
            if entry.key == key:
                if prev is None:
                    self.table[index] = entry.next
                else:
                    prev.next = entry.next
                self.count -= 1

                # encoger si el factor de carga cae demasiado
                if self.load_factor <= self.LOAD_FACTOR_SHRINK:
                    self._rehash(self.size // 2)
                return True
            prev  = entry
            entry = entry.next

        return False

    # ── Utilidades ────────────────────────────
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

    def __repr__(self):
        return (f"HashTable(size={self.size}, count={self.count}, "
                f"load_factor={self.load_factor:.2f})")


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