from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse, urljoin

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

def _is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@auth_bp.route("/login", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            next_url = request.args.get("next")
            if next_url and _is_safe_url(next_url):
                return redirect(next_url)
            return redirect(url_for("groups.group_list"))

        flash("Login fehlgeschlagen.", "error")

    return render_template("login/html/login.html")

@auth_bp.route("/test")
def test():
    return render_template("test.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_form():
    if request.method == "POST":
        # Registrierung (hast du schon)
        ...
        return redirect(url_for("auth.login_form"))

    return render_template("register/html/register.html")



@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Abgemeldet.", "success")
    return redirect(url_for("auth.login_form"))