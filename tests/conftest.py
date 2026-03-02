import os
import sys
import pytest
import uuid
from datetime import datetime, timezone

# 1. Fügt das Hauptverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.group import Group

@pytest.fixture
def app():
    """Erstellt eine Flask-Instanz für die Tests."""
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "super-geheimes-test-passwort", # Fixt den "session is unavailable" Fehler
    })

    with app.app_context():
        db.create_all()
        yield app       # <-- Wichtig: Das steht hier jetzt nur noch ein einziges Mal!
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Ein simulierter Browser für deine Routen."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Erstellt einen Standard-User für die Tests."""
    user_id_bytes = uuid.uuid4().bytes

    user = User(
        user_id=user_id_bytes,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="dummy_password_123", # Fixt den "NOT NULL constraint" Fehler
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_group(app, test_user):
    """Erstellt eine Standard-Gruppe für die Tests."""
    # Wandelt die Bytes der test_user ID zurück in einen String für die Group
    leader_id_string = str(uuid.UUID(bytes=test_user.user_id))

    group = Group(
        group_id=str(uuid.uuid4()),
        name="Test Gruppe",
        leader_id=leader_id_string,
        is_cross_class=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.session.add(group)
    db.session.commit()
    return group