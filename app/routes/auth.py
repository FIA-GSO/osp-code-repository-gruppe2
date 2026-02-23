from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
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
    
    print("METHOD:", request.method)
    print("FORM:", dict(request.form))
    
    


    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        print("user:", user)
        if user:
            print("stored pw:", user.password)
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            
            print("LOGIN OK -> current_user.is_authenticated =", current_user.is_authenticated)
            print("LOGIN OK -> current_user.get_id() =", current_user.get_id())

            return redirect(url_for("groups.group_list"))
        else:
            print("LOGIN FAIL -> user found? ", bool(user))
            if user: 
                print("Stored passwort start:", str(user.password)[:30])
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