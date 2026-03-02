import pytest
from flask import url_for
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User
from app.models.school_class import SchoolClass

# ==========================================
# LOKALE FIXTURES FÜR AUTH-TESTS
# ==========================================

@pytest.fixture
def test_school_class(app):
    """Erstellt eine Dummy-Schulklasse für die Registrierung."""
    sc = SchoolClass(id=1, name="10A")
    db.session.add(sc)
    db.session.commit()
    return sc

@pytest.fixture
def auth_user(app):
    """
    Erstellt einen User mit einem korrekt gehashten Passwort,
    damit check_password_hash() im Login funktioniert.
    """
    user = User(
        email="schueler@gso.schule.koeln",
        password=generate_password_hash("SicheresPasswort123!"),
        first_name="Max",
        last_name="Mustermann",
        role="user",
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return user


# ==========================================
# TESTS FÜR /login
# ==========================================

def test_login_form_renders(client):
    """Prüft, ob die Login-Seite (GET) lädt."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"E-Mail" in response.data

def test_login_success(client, auth_user):
    """Prüft den erfolgreichen Login mit korrekten Daten."""
    data = {
        "email": "schueler@gso.schule.koeln",
        "password": "SicheresPasswort123!"
    }
    response = client.post("/login", data=data)

    # Bei Erfolg leitet auth.py zu groups.group_list weiter (Status 302)
    assert response.status_code == 302
    assert "/groups" in response.headers["Location"]

def test_login_failure_wrong_password(client, auth_user):
    """Prüft den Login mit falschem Passwort."""
    data = {
        "email": "schueler@gso.schule.koeln",
        "password": "FalschesPasswort!"
    }
    response = client.post("/login", data=data)

    # Bei Fehler gibt auth.py Status 401 (Unauthorized) zurück
    assert response.status_code == 401
    assert b"E-Mail oder Passwort ist falsch" in response.data


# ==========================================
# TESTS FÜR /register
# ==========================================

def test_register_form_renders(client, test_school_class):
    """Prüft, ob die Registrierungs-Seite lädt und Schulklassen anzeigt."""
    response = client.get("/register")
    assert response.status_code == 200
    # Die Schulklasse "10A" sollte im HTML als Option auftauchen
    assert b"10A" in response.data

def test_register_success(client, test_school_class):
    """Prüft eine komplett fehlerfreie Registrierung."""
    data = {
        "school_class_id": test_school_class.id,
        "first_name": "Anna",
        "last_name": "Musterfrau",
        "email": "anna@gso.schule.koeln",
        "password": "SuperSicher123!" # Erfüllt alle Kriterien
    }
    response = client.post("/register", data=data)

    # Weiterleitung zur Erfolgsseite
    assert response.status_code == 302
    assert "/registerSuccess" in response.headers["Location"]

    # Überprüfen, ob Anna wirklich in der Datenbank gelandet ist
    new_user = User.query.filter_by(email="anna@gso.schule.koeln").first()
    assert new_user is not None
    assert new_user.first_name == "Anna"
    assert new_user.school_class_id == test_school_class.id

def test_register_invalid_email_domain(client, test_school_class):
    """Prüft, ob Fremd-E-Mails (z.B. gmail) geblockt werden."""
    data = {
        "school_class_id": test_school_class.id,
        "first_name": "Hacker",
        "last_name": "Man",
        "email": "hacker@gmail.com", # Falsche Domain!
        "password": "SuperSicher123!"
    }
    response = client.post("/register", data=data)

    # Gibt bei Fehlern ein 422 Unprocessable Entity zurück
    assert response.status_code == 422
    assert b"Bitte nutze deine GSO E-Mail-Adresse (@gso.schule.koeln)" in response.data

def test_register_weak_password(client, test_school_class):
    """Prüft, ob zu schwache Passwörter abgelehnt werden."""
    data = {
        "school_class_id": test_school_class.id,
        "first_name": "Kevin",
        "last_name": "Klein",
        "email": "kevin@gso.schule.koeln",
        "password": "hallo" # Viel zu kurz, keine Zahlen, keine Sonderzeichen
    }
    response = client.post("/register", data=data)

    assert response.status_code == 422
    assert b"Mindestens 8 Zeichen" in response.data


# ==========================================
# TESTS FÜR /logout
# ==========================================

def test_logout(client, auth_user):
    """Prüft, ob der Logout den User abmeldet und weiterleitet."""
    # 1. Zuerst einloggen, damit eine Session existiert
    client.post("/login", data={
        "email": "schueler@gso.schule.koeln",
        "password": "SicheresPasswort123!"
    })

    # 2. Dann ausloggen
    response = client.get("/logout")

    # Sollte zum Login redirecten
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]