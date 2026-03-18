from persistence.hash_table import HashTable

MAX_ENTRIES = 10


def obtener_ranking_global(dificultad):
    from crud.player import get_manager
    mgr = get_manager()

    entradas = []
    for nombre, player in mgr.players.items():
        scores = player.rankings.get(dificultad)
        if scores:
            entradas.append((nombre, max(scores)))

    entradas.sort(key=lambda e: e[1], reverse=True)
    return entradas[:MAX_ENTRIES]


def obtener_todos_los_rankings():
    ht = HashTable(size=16)
    ht.put("facil", obtener_ranking_global("facil"))
    ht.put("medio", obtener_ranking_global("medio"))
    ht.put("dificil", obtener_ranking_global("dificil"))
    return ht
