from __future__ import annotations

from datetime import datetime


RESOURCE_TYPES = [
    "Apuntes",
    "Resumen",
    "Ejercicios",
    "Examen",
    "Enlace",
]


class Resource:
    def __init__(self, title: str, description: str, resource_type: str, url: str, subject_id: str, author_id: str):
        self.title = title.strip()
        self.description = description.strip()
        self.resource_type = resource_type.strip()
        self.url = url.strip()
        self.subject_id = subject_id
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


def resources_for_subject(sr, subject_safe_id: str):
    resources = list(sr.filter(Resource, lambda r: r.subject_id == subject_safe_id))
    return sorted(resources, key=lambda r: r.created_at, reverse=True)


def resources_for_author(sr, author_safe_id: str):
    resources = list(sr.filter(Resource, lambda r: r.author_id == author_safe_id))
    return sorted(resources, key=lambda r: r.created_at, reverse=True)


def latest_resources(sr, limit: int = 6):
    resources = list(sr.load_all(Resource))
    resources.sort(key=lambda r: r.created_at, reverse=True)
    return resources[:limit]


def filtered_resources(sr, query: str = "", resource_type: str = "", subject_id: str = ""):
    query = query.strip().lower()
    resource_type = resource_type.strip()
    subject_id = subject_id.strip()

    resources = list(sr.load_all(Resource))
    results = []
    for resource in resources:
        if query and query not in resource.title.lower() and query not in resource.description.lower():
            continue
        if resource_type and resource.resource_type != resource_type:
            continue
        if subject_id and resource.subject_id != subject_id:
            continue
        results.append(resource)

    results.sort(key=lambda r: r.created_at, reverse=True)
    return results
