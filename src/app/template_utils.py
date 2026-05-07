from app.helpers import average_rating_for_resource, comments_count_for_resource, load_from_safe, safe_id


def register_template_utils(app):
    @app.context_processor
    def inject_helpers():
        return {
            "safe_id": safe_id,
            "load_from_safe": load_from_safe,
            "average_rating_for_resource": average_rating_for_resource,
            "comments_count_for_resource": comments_count_for_resource,
        }
