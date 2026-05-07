from flask import Blueprint, render_template

from app.resources.model import Resource, latest_resources
from app.storage import get_sirope
from app.subjects.model import Subject
from app.auth.model import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    sr = get_sirope()
    resources = latest_resources(sr, 6)
    stats = {
        "usuarios": sr.num_objs(User),
        "asignaturas": sr.num_objs(Subject),
        "recursos": sr.num_objs(Resource),
    }
    return render_template("main/index.html", resources=resources, stats=stats)
