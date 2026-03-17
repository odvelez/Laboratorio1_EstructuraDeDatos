from datetime import datetime

import save_system

jugador_actual = None


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

    def registrar_o_login(self, nombre):
        global jugador_actual

        players = self.datos.get("players", {})

        if nombre in players:
            jugador_actual = Player.from_dict(nombre, players[nombre])
        else:
            jugador_actual = Player(nombre)
            players[nombre] = jugador_actual.to_dict()
            self.datos["players"] = players
            self._guardar()

        return jugador_actual

    def registrar_intento(self, score, dificultad):
        if jugador_actual is None:
            return

        jugador_actual.registrar_intento(score, dificultad)
        self.datos["players"][jugador_actual.nombre] = jugador_actual.to_dict()
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
