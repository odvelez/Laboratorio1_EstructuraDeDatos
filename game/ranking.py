import save_system

MAX_ENTRIES = 10


def obtener_ranking_global(dificultad):
    datos = save_system.cargar_datos()
    players = datos.get("players", {})

    entradas = []
    for nombre, info in players.items():
        rankings = info.get("rankings", {})
        scores = rankings.get(dificultad, [])
        if scores:
            entradas.append((nombre, max(scores)))

    entradas.sort(key=lambda e: e[1], reverse=True)
    return entradas[:MAX_ENTRIES]


def obtener_todos_los_rankings():
    return {
        "facil": obtener_ranking_global("facil"),
        "medio": obtener_ranking_global("medio"),
        "dificil": obtener_ranking_global("dificil"),
    }
