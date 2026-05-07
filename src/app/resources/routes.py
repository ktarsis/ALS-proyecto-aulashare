from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.comments.model import comments_for_resource
from app.helpers import is_authenticated_owner, require_existing, safe_id
from app.ratings.model import ratings_for_resource
from app.resources.model import RESOURCE_TYPES, Resource, filtered_resources, resources_for_author
from app.storage import get_sirope
from app.subjects.model import all_subjects

resources_bp = Blueprint("resources", __name__, url_prefix="/resources")


@resources_bp.route("/")
def list_resources():
    sr = get_sirope()
    query = request.args.get("q", "")
    resource_type = request.args.get("type", "")
    subject_id = request.args.get("subject_id", "")

    resources = filtered_resources(sr, query=query, resource_type=resource_type, subject_id=subject_id)
    subjects = all_subjects(sr)
    return render_template(
        "resources/list.html",
        resources=resources,
        resource_types=RESOURCE_TYPES,
        subjects=subjects,
        filters={"q": query, "type": resource_type, "subject_id": subject_id},
    )


@resources_bp.route("/mine")
@login_required
def my_resources():
    resources = resources_for_author(get_sirope(), current_user.get_id())
    return render_template("resources/mine.html", resources=resources)


@resources_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_resource():
    sr = get_sirope()
    subjects = all_subjects(sr)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        resource_type = request.form.get("resource_type", "").strip()
        url = request.form.get("url", "").strip()
        subject_id = request.form.get("subject_id", "").strip()

        if len(title) < 3:
            flash("El titulo debe tener al menos 3 caracteres.", "danger")
        elif resource_type not in RESOURCE_TYPES:
            flash("Selecciona un tipo valido.", "danger")
        elif not url.startswith("http://") and not url.startswith("https://"):
            flash("La URL debe empezar por http:// o https://.", "danger")
        elif require_existing(subject_id) is None:
            flash("La asignatura indicada no existe.", "danger")
        else:
            resource = Resource(
                title=title,
                description=description,
                resource_type=resource_type,
                url=url,
                subject_id=subject_id,
                author_id=current_user.get_id(),
            )
            sr.save(resource)
            flash("Recurso creado correctamente.", "success")
            return redirect(url_for("resources.resource_detail", resource_id=safe_id(resource)))

    return render_template("resources/form.html", resource=None, resource_types=RESOURCE_TYPES, subjects=subjects)


@resources_bp.route("/<resource_id>")
def resource_detail(resource_id: str):
    sr = get_sirope()
    resource = require_existing(resource_id)
    comments = comments_for_resource(sr, resource_id)
    ratings = ratings_for_resource(sr, resource_id)
    return render_template("resources/detail.html", resource=resource, comments=comments, ratings=ratings)


@resources_bp.route("/<resource_id>/edit", methods=["GET", "POST"])
@login_required
def edit_resource(resource_id: str):
    sr = get_sirope()
    resource = require_existing(resource_id)
    if not is_authenticated_owner(resource.author_id):
        flash("No puedes editar este recurso.", "danger")
        return redirect(url_for("resources.resource_detail", resource_id=resource_id))

    subjects = all_subjects(sr)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        resource_type = request.form.get("resource_type", "").strip()
        url = request.form.get("url", "").strip()
        subject_id = request.form.get("subject_id", "").strip()

        if len(title) < 3:
            flash("El titulo debe tener al menos 3 caracteres.", "danger")
        elif resource_type not in RESOURCE_TYPES:
            flash("Selecciona un tipo valido.", "danger")
        elif not url.startswith("http://") and not url.startswith("https://"):
            flash("La URL debe empezar por http:// o https://.", "danger")
        else:
            resource.title = title
            resource.description = description
            resource.resource_type = resource_type
            resource.url = url
            resource.subject_id = subject_id
            from datetime import datetime
            resource.updated_at = datetime.utcnow()
            sr.save(resource)
            flash("Recurso actualizado.", "success")
            return redirect(url_for("resources.resource_detail", resource_id=resource_id))

    return render_template("resources/form.html", resource=resource, resource_types=RESOURCE_TYPES, subjects=subjects)


def _delete_resource_and_related(sr, resource, resource_id: str):
    comments = comments_for_resource(sr, resource_id)
    ratings = ratings_for_resource(sr, resource_id)
    oids = [c.__oid__ for c in comments] + [r.__oid__ for r in ratings] + [resource.__oid__]
    sr.multi_delete(oids)


@resources_bp.route("/<resource_id>/delete", methods=["POST"])
@login_required
def delete_resource(resource_id: str):
    sr = get_sirope()
    resource = require_existing(resource_id)
    if not is_authenticated_owner(resource.author_id):
        flash("No puedes borrar este recurso.", "danger")
        return redirect(url_for("resources.resource_detail", resource_id=resource_id))

    _delete_resource_and_related(sr, resource, resource_id)
    flash("Recurso eliminado.", "success")
    return redirect(url_for("resources.list_resources"))


@resources_bp.route("/<resource_id>/delete-inline", methods=["POST"])
@login_required
def delete_inline(resource_id: str):
    sr = get_sirope()
    resource = require_existing(resource_id)
    if not is_authenticated_owner(resource.author_id):
        return Response("", status=403)

    _delete_resource_and_related(sr, resource, resource_id)
    return Response("", status=204)
