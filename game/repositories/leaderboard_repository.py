"""
Leaderboard Repository - Gestión de rankings/puntajes

Usa el sistema de persistencia para guardar/cargar puntajes.
"""

from typing import List, Dict, Any, Optional
from persistence_system import PersistenceSystem


class LeaderboardRepository:
    """Repositorio para rankings y puntajes."""

    def __init__(self, persistence_system: PersistenceSystem):
        self.persistence = persistence_system

    def save_score(self, username: str, score: int, difficulty: str, timestamp: str = None) -> bool:
        import datetime
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        score_data = {
            "username": username,
            "score": score,
            "difficulty": difficulty,
            "timestamp": timestamp
        }

        key = f"score:{username}:{difficulty}:{timestamp}"
        return self.persistence.save(key, score_data, "score")

    def get_user_scores(self, username: str, difficulty: str) -> List[Dict[str, Any]]:
        scores = []
        prefix = f"score:{username}:{difficulty}:"
        for key in self.persistence.get_all_keys():
            if key.startswith(prefix):
                score_data = self.persistence.get(key)
                if score_data:
                    scores.append(score_data)
        scores.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return scores

    def get_leaderboard(self, difficulty: str, limit: int = 10) -> List[Dict[str, Any]]:
        scores = []
        for key in self.persistence.get_all_keys():
            if key.startswith("score:"):
                score_data = self.persistence.get(key)
                if score_data and score_data.get("difficulty") == difficulty:
                    scores.append(score_data)
        scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        return scores[:limit]

    def get_user_best_score(self, username: str, difficulty: str) -> Optional[int]:
        scores = self.get_user_scores(username, difficulty)
        if not scores:
            return None
        return max(score["score"] for score in scores)

    def get_global_stats(self) -> Dict[str, Any]:
        total_scores = 0
        difficulties = set()
        users = set()

        for key in self.persistence.get_all_keys():
            if key.startswith("score:"):
                score_data = self.persistence.get(key)
                if score_data:
                    total_scores += 1
                    difficulties.add(score_data.get("difficulty", ""))
                    users.add(score_data.get("username", ""))

        return {
            "total_scores": total_scores,
            "unique_users": len(users),
            "difficulties": list(difficulties)
        }
