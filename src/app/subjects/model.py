from __future__ import annotations

from datetime import datetime


class Subject:
    def __init__(self, name: str, degree: str, course: str, description: str, creator_id: str):
        self.name = name.strip()
        self.degree = degree.strip()
        self.course = course.strip()
        self.description = description.strip()
        self.creator_id = creator_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


def all_subjects(sr):
    return sorted(
        list(sr.load_all(Subject)),
        key=lambda s: (s.degree.lower(), s.course.lower(), s.name.lower()),
    )
