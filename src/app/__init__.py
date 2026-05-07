from flask import Flask, render_template

from app.auth.routes import auth_bp
from app.comments.routes import comments_bp
from app.extensions import init_login_manager
from app.main.routes import main_bp
from app.ratings.routes import ratings_bp
from app.resources.routes import resources_bp
from app.subjects.routes import subjects_bp
from app.template_utils import register_template_utils


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    init_login_manager(app)
    register_template_utils(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(ratings_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", title="No encontrado", message="La pagina que buscas no existe o el recurso ha sido eliminado."), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return render_template("error.html", title="Error interno", message="Se produjo un error inesperado. Puedes volver al inicio e intentarlo de nuevo."), 500

    return app
