from flask import flash, redirect, url_for
from flask_login import LoginManager

from app.auth.model import User
from app.storage import get_sirope

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesion para acceder a esa pagina."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id: str):
    sr = get_sirope()
    oid = sr.oid_from_safe(user_id)
    if oid is None or not sr.exists(oid):
        return None
    try:
        return sr.load(oid)
    except Exception:
        return None


def init_login_manager(app):
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        flash("Necesitas iniciar sesion para continuar.", "warning")
        return redirect(url_for("auth.login"))
