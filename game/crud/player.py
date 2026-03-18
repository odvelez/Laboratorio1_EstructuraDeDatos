from datetime import datetime

from crud import save_system
from persistence.hash_table import HashTable, hash_string

jugador_actual = None


def _hash_password(password):
    return hash_string(password)


class Player:
    def __init__(self, nombre, max_score=0, attempts=None,
                 rankings=None, password=""):
        self.nombre    = nombre
        self.max_score = max_score
        self.attempts  = attempts if attempts is not None else []
        self.password  = password

        self.rankings = HashTable(size=16)
        if rankings is not None:
            for dif, scores in rankings:
                self.rankings.put(dif, list(scores))
        else:
            self.rankings.put("facil", [])
            self.rankings.put("medio", [])
            self.rankings.put("dificil", [])

    def get_nombre(self):
        return self.nombre

    def get_max_score(self):
        return self.max_score

    def get_intentos(self):
        return list(self.attempts)

    def get_ranking(self, dificultad):
        result = self.rankings.get(dificultad)
        return list(result) if result is not None else []

    def registrar_intento(self, score, dificultad):
        intento = (score,
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   dificultad)
        self.attempts.append(intento)

        if score > self.max_score:
            self.max_score = score

        scores = self.rankings.get(dificultad)
        if scores is None:
            scores = []
        scores.append(score)
        scores.sort(reverse=True)
        self.rankings.put(dificultad, scores[:10])

    def to_dict(self):
        """Serialización → estructura compatible con JSON."""
        rankings_out = {}
        for dif, scores in self.rankings.items():
            rankings_out[dif] = scores

        attempts_out = []
        for a in self.attempts:
            if isinstance(a, (list, tuple)):
                attempts_out.append({
                    "score": a[0],
                    "fecha": a[1],
                    "dificultad": a[2],
                })
            else:
                attempts_out.append(a)

        return {
            "maxScore": self.max_score,
            "attempts": attempts_out,
            "rankings": rankings_out,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, nombre, data):
        """Deserialización ← estructura JSON."""
        rankings_raw = data.get("rankings", {})
        rankings_items = list(rankings_raw.items())

        attempts_raw = data.get("attempts", [])
        attempts = []
        for a in attempts_raw:
            if isinstance(a, (list, tuple)):
                attempts.append(tuple(a))
            else:
                attempts.append((
                    a.get("score", 0),
                    a.get("fecha", ""),
                    a.get("dificultad", ""),
                ))

        return cls(
            nombre=nombre,
            max_score=data.get("maxScore", 0),
            attempts=attempts,
            rankings=rankings_items,
            password=data.get("password", ""),
        )


class PlayerManager:
    def __init__(self):
        self.players = HashTable(size=16)
        raw = save_system.cargar_datos()
        players_raw = raw.get("players", {}) if isinstance(raw, (dict,)) else {}
        for nombre in players_raw:
            player = Player.from_dict(nombre, players_raw[nombre])
            self.players.put(nombre, player)

    def register_user(self, username, password):
        if self.players.contains(username):
            existing = self.players.get(username)
            if existing.password:
                return None, "Username already exists"
            existing.password = _hash_password(password)
            self._guardar()
            return existing, ""

        nuevo = Player(nombre=username, password=_hash_password(password))
        self.players.put(username, nuevo)
        self._guardar()
        return nuevo, ""

    def login_user(self, username, password):
        if not self.players.contains(username):
            return None, "User not found"

        player = self.players.get(username)
        if not player.password:
            return None, "Account has no password, register again"

        if not self.validate_user(username, password):
            return None, "Incorrect password"

        return player, ""

    def validate_user(self, username, password):
        if not self.players.contains(username):
            return False
        player = self.players.get(username)
        return player.password == _hash_password(password)

    def set_jugador_actual(self, jugador):
        global jugador_actual
        jugador_actual = jugador

    def registrar_intento(self, score, dificultad):
        if jugador_actual is None:
            return
        jugador_actual.registrar_intento(score, dificultad)
        self._guardar()

    def get_jugador_actual(self):
        return jugador_actual

    def _guardar(self):
        """Serializa el HashTable de jugadores a JSON."""
        players_out = {}
        for nombre, player_obj in self.players.items():
            players_out[nombre] = player_obj.to_dict()
        save_system.guardar_datos({"players": players_out})


manager = None


def inicializar():
    global manager
    manager = PlayerManager()


def get_manager():
    if manager is None:
        inicializar()
    return manager
