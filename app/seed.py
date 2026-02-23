import uuid
from datetime import datetime, UTC
from werkzeug.security import generate_password_hash

import os

from app import create_app
from app.extensions import db
from app.models.user import User

def seed_users():
    """Erstellt einen Admin-User, falls er noch nicht existiert"""
    user_email = "max.mustermann@gso.schule.koeln"

    if User.query.filter_by(email=user_email).first():
        print("⚠️ User existiert bereits – übersprungen")
        return

    user = User(
        user_id=uuid.uuid4().bytes,
        email=user_email,
        password=generate_password_hash("test123"),
        first_name="Max",
        last_name="Mustermann",
        role="user",
        is_active=True,
        created_at=datetime.now(UTC)
    )

    db.session.add(user)
    db.session.commit()
    print("✅ Admin-User erstellt (max.mustermann@gso.schule.koeln / test123)")


def seed_admin_user():
    """Erstellt einen Admin-User, falls er noch nicht existiert"""
    admin_email = "admin@example.com"

    if User.query.filter_by(email=admin_email).first():
        print("⚠️ Admin-User existiert bereits – übersprungen")
        return

    admin = User(
        user_id=uuid.uuid4().bytes,
        email=admin_email,
        password=generate_password_hash("admin123"),
        first_name="Admin",
        last_name="User",
        role="admin",
        is_active=True,
        created_at=datetime.now(UTC)
    )

    db.session.add(admin)
    db.session.commit()
    print("✅ Admin-User erstellt (admin@example.com / admin123)")


def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding gestartet...")
        seed_admin_user()
        seed_users()
        print("✅ Seeding abgeschlossen")


if __name__ == "__main__":
    seed()