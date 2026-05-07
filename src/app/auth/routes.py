from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth.model import User, find_user_by_email, find_user_by_username
from app.storage import get_sirope

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")

        if len(username) < 3:
            flash("El nombre de usuario debe tener al menos 3 caracteres.", "danger")
        elif "@" not in email or "." not in email:
            flash("Introduce un email valido.", "danger")
        elif len(password) < 4:
            flash("La contrasena debe tener al menos 4 caracteres.", "danger")
        elif password != password2:
            flash("Las contrasenas no coinciden.", "danger")
        else:
            sr = get_sirope()
            if find_user_by_username(sr, username):
                flash("Ese nombre de usuario ya existe.", "danger")
            elif find_user_by_email(sr, email):
                flash("Ese email ya esta registrado.", "danger")
            else:
                user = User(username=username, email=email, password=password)
                sr.save(user)
                login_user(user)
                flash("Cuenta creada correctamente.", "success")
                return redirect(url_for("main.index"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        sr = get_sirope()
        user = find_user_by_email(sr, email)
        if user is None or not user.check_password(password):
            flash("Credenciales incorrectas.", "danger")
        else:
            login_user(user)
            flash("Sesion iniciada correctamente.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesion cerrada.", "success")
    return redirect(url_for("main.index"))
