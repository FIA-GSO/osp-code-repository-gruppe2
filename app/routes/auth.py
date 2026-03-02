import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.user import User
from app.models.school_class import SchoolClass

auth_bp = Blueprint("auth", __name__)

GSO_DOMAIN = "@gso.schule.koeln"
MIN_PW_LEN = 8


def is_fetch_request() -> bool:
    """Erkennt AJAX/fetch Requests aus unserem Frontend."""
    return request.headers.get("X-Requested-With") == "fetch"


def valid_name(name: str) -> bool:
    """
    Nur Buchstaben + Leerzeichen/Bindestrich.
    Nutzt Unicode isalpha() => Umlaute/ß funktionieren.
    """
    if not name:
        return False
    allowed_extra = {" ", "-"}
    for ch in name:
        if ch.isalpha():
            continue
        if ch in allowed_extra:
            continue
        return False
    # nicht nur aus Leerzeichen/Bindestrich bestehen
    return any(c.isalpha() for c in name)


def validate_password(pw: str) -> list[str]:
    """Liste von Passwort-Fehlermeldungen (leer = ok)."""
    errors = []
    if len(pw) < 8:
        errors.append("Mindestens 8 Zeichen.")
    if not re.search(r"[a-z]", pw):
        errors.append("Mindestens ein Kleinbuchstabe.")
    if not re.search(r"[A-Z]", pw):
        errors.append("Mindestens ein Großbuchstabe.")
    if not re.search(r"\d", pw):
        errors.append("Mindestens eine Zahl.")
    if not re.search(r"[^A-Za-z0-9]", pw):
        errors.append("Mindestens ein Sonderzeichen.")
    return errors



def validate_login_inputs(email: str, password: str) -> dict:
    errors = {}

    # Email required + basic plausibility + domain
    if not email:
        errors["email"] = "E-Mail ist erforderlich."
    else:
        lower = email.lower()
        # minimale Plausi (nicht zu streng, Login ist kein Register)
        if "@" not in lower or lower.startswith("@") or lower.endswith("@"):
            errors["email"] = "Bitte eine gültige E-Mail-Adresse eingeben."
        elif not lower.endswith(GSO_DOMAIN):
            errors["email"] = f"Bitte nutze deine GSO E-Mail-Adresse ({GSO_DOMAIN})."

    # Password required + min length
    if not password:
        errors["password"] = "Passwort ist erforderlich."
    elif len(password) < MIN_PW_LEN:
        errors["password"] = f"Das Passwort muss mindestens {MIN_PW_LEN} Zeichen lang sein."

    return errors



@auth_bp.route("/login", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        remember = bool(request.form.get("remember"))

        # Optional: wenn du wirklich jeden Submit versuchen willst (auch leer),
        # lass es wie hier. Kein Feldfehler, nur generisch.
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for("groups.group_list"))

        # ❗ Nur EIN Fehlertext, immer gleich
        return render_template(
            "login/html/login.html",
            errors={"general": "E-Mail oder Passwort ist falsch."},
            form={"email": email}
        ), 401

    return render_template("login/html/login.html")






@auth_bp.route("/register", methods=["GET", "POST"])
def register_form():
    classes = SchoolClass.query.order_by(SchoolClass.name.asc()).all()

    if request.method == "GET":
        return render_template("register/html/register.html", classes=classes)

    # POST
    school_class_id = (request.form.get("school_class_id") or "").strip()
    first_name = (request.form.get("first_name") or "").strip()
    last_name  = (request.form.get("last_name") or "").strip()
    email      = (request.form.get("email") or "").strip().lower()
    password   = request.form.get("password") or ""

    errors = {}

    # Klasse required + existiert
    sc_id = None
    if not school_class_id:
        errors["school_class_id"] = "Bitte wähle eine Klasse aus."
    else:
        try:
            sc_id = int(school_class_id)
            if not SchoolClass.query.get(sc_id):
                errors["school_class_id"] = "Ungültige Klasse ausgewählt."
        except ValueError:
            errors["school_class_id"] = "Ungültige Klasse ausgewählt."

    # Vorname / Nachname required + nur Buchstaben
    if not first_name:
        errors["first_name"] = "Vorname ist erforderlich."
    elif not valid_name(first_name):
        errors["first_name"] = "Nur Buchstaben (ggf. Leerzeichen/Bindestrich) erlaubt."

    if not last_name:
        errors["last_name"] = "Nachname ist erforderlich."
    elif not valid_name(last_name):
        errors["last_name"] = "Nur Buchstaben (ggf. Leerzeichen/Bindestrich) erlaubt."

    # Email: required + Domain + Unique
    if not email:
        errors["email"] = "E-Mail ist erforderlich."
    else:
        # einfache Plausi (optional)
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            errors["email"] = "Bitte eine gültige E-Mail-Adresse eingeben."
        elif not email.endswith("@gso.schule.koeln"):
            errors["email"] = "Bitte nutze deine GSO E-Mail-Adresse (@gso.schule.koeln)."
        elif User.query.filter_by(email=email).first():
            errors["email"] = "Diese E-Mail ist bereits registriert."

    # Passwort Standards
    if not password:
        errors["password"] = "Passwort ist erforderlich."
    else:
        pw_errors = validate_password(password)
        if pw_errors:
            errors["password"] = pw_errors

    # Fehler -> JSON für fetch / HTML fallback
    if errors:
        if is_fetch_request():
            return jsonify({"ok": False, "errors": errors}), 422

        # Fallback wenn JS aus: Seite rendern (kein redirect)
        return render_template(
            "register/html/register.html",
            classes=classes,
            errors=errors,
            form={
                "school_class_id": school_class_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        ), 422

    # User erstellen
    user = User(
        email=email,
        password=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        role="user",
        is_active=True,
        school_class_id=sc_id
    )
    db.session.add(user)
    db.session.commit()
    # Erfolg: JSON redirect oder normaler redirect
    if is_fetch_request():
        return jsonify({"ok": True, "redirect": url_for("auth.register_success")}), 200

    return redirect(url_for("auth.register_success"))

@auth_bp.route("/registerSuccess", methods=["GET"])
def register_success():
    return render_template("registerSuccess/html/registerSuccess.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Abgemeldet.", "success")
    return redirect(url_for("auth.login_form"))