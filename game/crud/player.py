from datetime import datetime

from crud import save_system
from persistence.hash_table import hash_string

jugador_actual = None


def _hash_password(password):
    return hash_string(password)


class Player:
    def __init__(self, nombre, max_score=0, attempts=None, rankings=None):
        self.nombre = nombre
        self.max_score = max_score
        self.attempts = attempts if attempts is not None else []
        self.rankings = rankings if rankings is not None else {
            "facil": [],
            "medio": [],
            "dificil": [],
        }

    def get_nombre(self):
        return self.nombre

    def get_max_score(self):
        return self.max_score

    def get_intentos(self):
        return list(self.attempts)

    def get_ranking(self, dificultad):
        return list(self.rankings.get(dificultad, []))

    def registrar_intento(self, score, dificultad):
        intento = {
            "score": score,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dificultad": dificultad,
        }
        self.attempts.append(intento)

        if score > self.max_score:
            self.max_score = score

        if dificultad not in self.rankings:
            self.rankings[dificultad] = []
        self.rankings[dificultad].append(score)
        self.rankings[dificultad].sort(reverse=True)
        self.rankings[dificultad] = self.rankings[dificultad][:10]

    def to_dict(self):
        return {
            "maxScore": self.max_score,
            "attempts": self.attempts,
            "rankings": self.rankings,
        }

    @classmethod
    def from_dict(cls, nombre, data):
        return cls(
            nombre=nombre,
            max_score=data.get("maxScore", 0),
            attempts=data.get("attempts", []),
            rankings=data.get("rankings", {
                "facil": [],
                "medio": [],
                "dificil": [],
            }),
        )


class PlayerManager:
    def __init__(self):
        self.datos = save_system.cargar_datos()

    def register_user(self, username, password):
        players = self.datos.get("players", {})

        if username in players:
            existing = players[username]
            if existing.get("password", ""):
                return None, "Username already exists"
            existing["password"] = _hash_password(password)
            self._guardar()
            return Player.from_dict(username, existing), ""

        hashed = _hash_password(password)
        nuevo = Player(username)
        players[username] = nuevo.to_dict()
        players[username]["password"] = hashed
        self.datos["players"] = players
        self._guardar()

        return nuevo, ""

    def login_user(self, username, password):
        players = self.datos.get("players", {})

        if username not in players:
            return None, "User not found"

        stored = players[username].get("password", "")
        if not stored:
            return None, "Account has no password, register again"

        if not self.validate_user(username, password):
            return None, "Incorrect password"

        return Player.from_dict(username, players[username]), ""

    def validate_user(self, username, password):
        players = self.datos.get("players", {})
        if username not in players:
            return False

        stored = players[username].get("password", "")
        return stored == _hash_password(password)

    def set_jugador_actual(self, jugador):
        global jugador_actual
        jugador_actual = jugador

    def registrar_intento(self, score, dificultad):
        if jugador_actual is None:
            return

        jugador_actual.registrar_intento(score, dificultad)
        player_data = jugador_actual.to_dict()
        player_data["password"] = self.datos["players"][jugador_actual.nombre].get("password", "")
        self.datos["players"][jugador_actual.nombre] = player_data
        self._guardar()

    def get_jugador_actual(self):
        return jugador_actual

    def _guardar(self):
        save_system.guardar_datos(self.datos)


manager = None


def inicializar():
    global manager
    manager = PlayerManager()


def get_manager():
    if manager is None:
        inicializar()
    return manager
