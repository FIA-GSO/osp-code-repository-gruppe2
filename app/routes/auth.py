from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse, urljoin

from app.models.school_class import SchoolClass

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
    
    print("REGISTER METHOD:", request.method)
    print("REGISTER FORM:", request.form.to_dict())

    if request.method == "POST":
        # Form auslesen
        school_class_id = request.form.get("school_class_id", "")
        first_name = request.form.get("first_name", "").strip()
        last_name  = request.form.get("last_name", "").strip()
        email      = request.form.get("email", "").strip().lower()
        password   = request.form.get("password", "")

        # Validierung
        if not first_name or not last_name or not email or not password:
            flash("Bitte fülle alle Pflichtfelder aus.", "error")
            return redirect(url_for("auth.register_form"))

        # Optional: Domain-Check
        # if not email.endswith("@gso.schule.koeln"):
        #     flash("Bitte nutze deine GSO E-Mail-Adresse.", "error")
        #     return redirect(url_for("auth.register_form"))

        # Email unique
        if User.query.filter_by(email=email).first():
            flash("Diese E-Mail ist bereits registriert.", "error")
            return redirect(url_for("auth.register_form"))

        # school_class_id optional, aber wenn gesetzt -> prüfen
        sc_id = None
        if school_class_id:
            try:
                sc_id = int(school_class_id)
            except ValueError:
                sc_id = None

            if sc_id and not SchoolClass.query.get(sc_id):
                flash("Ungültige Klasse ausgewählt.", "error")
                return redirect(url_for("auth.register_form"))

        # User erstellen (WICHTIG: Passwort hashen)
        user = User(
            email=email,
            password=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role="user",
            is_active=True,
            school_class_id=sc_id
        )
        print(user.first_name)
        db.session.add(user)
        db.session.commit()

        flash("Registrierung erfolgreich! Bitte logge dich ein.", "success")
        return redirect(url_for("auth.login_form"))

    # GET: Klassen für Dropdown laden
    classes = SchoolClass.query.order_by(SchoolClass.name.asc()).all()
    return render_template("register/html/register.html", classes=classes)




@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Abgemeldet.", "success")
    return redirect(url_for("auth.login_form"))