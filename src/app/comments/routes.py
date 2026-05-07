from flask import Blueprint, Response, flash, render_template
from flask_login import current_user, login_required

from app.comments.model import Comment, comments_for_resource
from app.helpers import is_authenticated_owner, require_existing, safe_id
from app.storage import get_sirope

comments_bp = Blueprint("comments", __name__, url_prefix="/comments")


@comments_bp.route("/resource/<resource_id>/create", methods=["POST"])
@login_required
def create_comment(resource_id: str):
    from flask import request

    sr = get_sirope()
    resource = require_existing(resource_id)
    text = request.form.get("text", "").strip()

    if len(text) < 2:
        flash("El comentario debe tener al menos 2 caracteres.", "danger")
    else:
        comment = Comment(text=text, resource_id=resource_id, author_id=current_user.get_id())
        sr.save(comment)
        flash("Comentario anadido.", "success")

    comments = comments_for_resource(sr, resource_id)
    return render_template("comments/_comments_section.html", resource=resource, comments=comments)


@comments_bp.route("/<comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id: str):
    sr = get_sirope()
    comment = require_existing(comment_id)

    if not is_authenticated_owner(comment.author_id):
        return Response("", status=403)

    resource_id = comment.resource_id
    resource = require_existing(resource_id)
    sr.delete(comment.__oid__)

    comments = comments_for_resource(sr, resource_id)
    return render_template("comments/_comments_section.html", resource=resource, comments=comments)
