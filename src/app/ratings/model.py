from __future__ import annotations

from datetime import datetime


class Rating:
    def __init__(self, score: int, resource_id: str, author_id: str):
        self.score = int(score)
        self.resource_id = resource_id
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


def ratings_for_resource(sr, resource_safe_id: str):
    return list(sr.filter(Rating, lambda r: r.resource_id == resource_safe_id))


def find_rating_for_user_and_resource(sr, author_safe_id: str, resource_safe_id: str):
    return sr.find_first(Rating, lambda r: r.author_id == author_safe_id and r.resource_id == resource_safe_id)


def average_rating_for_resource_model(sr, resource_safe_id: str) -> float:
    ratings = ratings_for_resource(sr, resource_safe_id)
    if not ratings:
        return 0.0
    return round(sum(r.score for r in ratings) / len(ratings), 2)
