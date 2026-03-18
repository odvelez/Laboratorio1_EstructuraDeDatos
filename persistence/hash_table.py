from persistence.hash_entry import HashEntry


class HashTable:
    """Tabla hash con encadenamiento separado (separate chaining).

    Implementada desde cero usando solo list, tuple, clases y archivos.

    Operaciones:
        put(key, value)   – Insertar o actualizar
        get(key, default) – Buscar por clave
        delete(key)       – Eliminar por clave

    Manejo automático de colisiones, factor de carga y rehash.
    """

    LOAD_FACTOR_GROW   = 0.75
    LOAD_FACTOR_SHRINK = 0.25
    MIN_SIZE           = 16

    def __init__(self, size=16):
        self.size  = max(size, self.MIN_SIZE)
        self.table = [None] * self.size
        self.count = 0

    # ── Factor de carga ───────────────────────────

    @property
    def load_factor(self):
        return self.count / self.size if self.size > 0 else 0.0

    # ── Función hash interna ──────────────────────

    def _hash(self, key):
        """Hash polinómico: h = sum(char_i * 31^i) mod size."""
        h = 0
        for char in str(key):
            h = (h * 31 + ord(char)) & 0xFFFFFFFF
        return h % self.size

    # ── Rehash / reconstrucción del índice ────────

    def _rehash(self, new_size):
        """Reconstruye toda la tabla con un nuevo tamaño,
        recalculando el índice de cada entrada."""
        new_size  = max(new_size, self.MIN_SIZE)
        old_items = self.items()

        self.size  = new_size
        self.table = [None] * self.size
        self.count = 0

        for key, value in old_items:
            self._insert(key, value)

    # ── Inserción interna (sin chequeo de carga) ─

    def _insert(self, key, value):
        index = self._hash(key)
        entry = self.table[index]

        while entry is not None:
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next

        new_entry      = HashEntry(key, value)
        new_entry.next = self.table[index]
        self.table[index] = new_entry
        self.count += 1

    # ── put(key, value_reference) ─────────────────

    def put(self, key, value):
        """Inserta o actualiza un par clave → valor.
        Si load_factor >= 0.75, hace rehash duplicando el tamaño."""
        self._insert(key, value)

        if self.load_factor >= self.LOAD_FACTOR_GROW:
            self._rehash(self.size * 2)

    # ── get(key) ──────────────────────────────────

    def get(self, key, default=None):
        """Retorna el valor asociado a key, o default si no existe."""
        index = self._hash(key)
        entry = self.table[index]

        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next

        return default

    # ── delete(key) ───────────────────────────────

    def delete(self, key):
        """Elimina el par con la clave dada.  Retorna True si se eliminó.
        Si load_factor <= 0.25, hace rehash reduciendo a la mitad."""
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

                if (self.size > self.MIN_SIZE
                        and self.load_factor <= self.LOAD_FACTOR_SHRINK):
                    self._rehash(self.size // 2)
                return True

            prev  = entry
            entry = entry.next

        return False

    remove = delete

    # ── contains ──────────────────────────────────

    def contains(self, key):
        return self.get(key) is not None

    # ── Iteradores ────────────────────────────────

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
    """Hash FNV-1a modificado para contraseñas.
    Retorna un string hexadecimal de 16 caracteres."""
    h1 = 0x811C9DC5
    h2 = 0x01000193

    for char in text:
        code = ord(char)
        h1 = ((h1 ^ code) * 0x01000193) & 0xFFFFFFFF
        h2 = ((h2 * 31) + code + h1) & 0xFFFFFFFF

    combined = ((h1 << 32) | h2) & 0xFFFFFFFFFFFFFFFF
    return format(combined, "016x")
