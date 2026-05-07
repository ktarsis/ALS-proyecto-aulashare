from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from app.helpers import require_existing
from app.ratings.model import Rating, average_rating_for_resource_model, find_rating_for_user_and_resource, ratings_for_resource
from app.storage import get_sirope

ratings_bp = Blueprint("ratings", __name__, url_prefix="/ratings")


@ratings_bp.route("/resource/<resource_id>/set", methods=["POST"])
@login_required
def set_rating(resource_id: str):
    sr = get_sirope()
    resource = require_existing(resource_id)

    try:
        score = int(request.form.get("score", "0"))
    except ValueError:
        score = 0

    if score < 1 or score > 5:
        flash("La puntuacion debe estar entre 1 y 5.", "danger")
    else:
        rating = find_rating_for_user_and_resource(sr, current_user.get_id(), resource_id)
        if rating is None:
            rating = Rating(score=score, resource_id=resource_id, author_id=current_user.get_id())
        else:
            rating.score = score
            from datetime import datetime
            rating.updated_at = datetime.utcnow()
        sr.save(rating)
        flash("Valoracion guardada.", "success")

    ratings = ratings_for_resource(sr, resource_id)
    average = average_rating_for_resource_model(sr, resource_id)
    user_rating = find_rating_for_user_and_resource(sr, current_user.get_id(), resource_id)
    return render_template("ratings/_rating_box.html", resource=resource, ratings=ratings, average=average, user_rating=user_rating)
