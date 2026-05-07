from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.helpers import is_authenticated_owner, require_existing, safe_id
from app.resources.model import resources_for_subject
from app.storage import get_sirope
from app.subjects.model import Subject, all_subjects

subjects_bp = Blueprint("subjects", __name__, url_prefix="/subjects")


@subjects_bp.route("/")
def list_subjects():
    subjects = all_subjects(get_sirope())
    return render_template("subjects/list.html", subjects=subjects)


@subjects_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_subject():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        degree = request.form.get("degree", "").strip()
        course = request.form.get("course", "").strip()
        description = request.form.get("description", "").strip()

        if len(name) < 3:
            flash("El nombre de la asignatura debe tener al menos 3 caracteres.", "danger")
        elif not degree:
            flash("Debes indicar un grado o categoria.", "danger")
        elif not course:
            flash("Debes indicar el curso.", "danger")
        else:
            subject = Subject(
                name=name,
                degree=degree,
                course=course,
                description=description,
                creator_id=current_user.get_id(),
            )
            get_sirope().save(subject)
            flash("Asignatura creada correctamente.", "success")
            return redirect(url_for("subjects.subject_detail", subject_id=safe_id(subject)))

    return render_template("subjects/form.html", subject=None)


@subjects_bp.route("/<subject_id>")
def subject_detail(subject_id: str):
    subject = require_existing(subject_id)
    resources = resources_for_subject(get_sirope(), subject_id)
    return render_template("subjects/detail.html", subject=subject, resources=resources)


@subjects_bp.route("/<subject_id>/edit", methods=["GET", "POST"])
@login_required
def edit_subject(subject_id: str):
    subject = require_existing(subject_id)
    if not is_authenticated_owner(subject.creator_id):
        flash("No puedes editar esta asignatura.", "danger")
        return redirect(url_for("subjects.subject_detail", subject_id=subject_id))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        degree = request.form.get("degree", "").strip()
        course = request.form.get("course", "").strip()
        description = request.form.get("description", "").strip()

        if len(name) < 3:
            flash("El nombre de la asignatura debe tener al menos 3 caracteres.", "danger")
        elif not degree or not course:
            flash("Debes completar grado y curso.", "danger")
        else:
            subject.name = name
            subject.degree = degree
            subject.course = course
            subject.description = description
            from datetime import datetime
            subject.updated_at = datetime.utcnow()
            get_sirope().save(subject)
            flash("Asignatura actualizada.", "success")
            return redirect(url_for("subjects.subject_detail", subject_id=subject_id))

    return render_template("subjects/form.html", subject=subject)


@subjects_bp.route("/<subject_id>/delete", methods=["POST"])
@login_required
def delete_subject(subject_id: str):
    sr = get_sirope()
    subject = require_existing(subject_id)
    if not is_authenticated_owner(subject.creator_id):
        flash("No puedes borrar esta asignatura.", "danger")
        return redirect(url_for("subjects.subject_detail", subject_id=subject_id))

    if resources_for_subject(sr, subject_id):
        flash("No se puede borrar una asignatura que aun tiene recursos asociados.", "warning")
        return redirect(url_for("subjects.subject_detail", subject_id=subject_id))

    sr.delete(subject.__oid__)
    flash("Asignatura eliminada.", "success")
    return redirect(url_for("subjects.list_subjects"))
