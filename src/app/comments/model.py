from __future__ import annotations

from datetime import datetime


class Comment:
    def __init__(self, text: str, resource_id: str, author_id: str):
        self.text = text.strip()
        self.resource_id = resource_id
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


def comments_for_resource(sr, resource_safe_id: str):
    comments = list(sr.filter(Comment, lambda c: c.resource_id == resource_safe_id))
    return sorted(comments, key=lambda c: c.created_at, reverse=True)
