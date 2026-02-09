import uuid
from datetime import datetime, UTC
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.school_class import SchoolClass


def seed_classes():
    """Erstellt alle Klassen, falls sie noch nicht existieren"""
    created = 0

    def ensure_class(name: str):
        nonlocal created
        if not SchoolClass.query.filter_by(name=name).first():
            db.session.add(
                SchoolClass(
                    class_id=str(uuid.uuid4()),
                    name=name,
                    is_active=True,
                    created_at=datetime.now(UTC)
                )
            )
            created += 1

    # FI<1-5><0-20>
    for year in range(1, 6):
        for number in range(0, 21):
            ensure_class(f"FI{year}{number}")

    # FIA<1-5><A-H>
    for year in range(1, 6):
        for letter in "ABCDEFGH":
            ensure_class(f"FIA{year}{letter}")

    # FIS<1-5><A-H>
    for year in range(1, 6):
        for letter in "ABCDEFGH":
            ensure_class(f"FIS{year}{letter}")

    db.session.commit()
    print(f"✅ {created} neue Klassen erstellt")


def seed_admin_user():
    """Erstellt einen Admin-User, falls er noch nicht existiert"""
    admin_email = "admin@example.com"

    if User.query.filter_by(email=admin_email).first():
        print("⚠️ Admin-User existiert bereits – übersprungen")
        return

    school_class = SchoolClass.query.filter_by(name="FI11").first()
    if not school_class:
        raise RuntimeError("❌ Klasse FI11 nicht gefunden (Seed-Reihenfolge falsch)")

    admin = User(
        user_id=uuid.uuid4().bytes,
        email=admin_email,
        password=generate_password_hash("admin123"),
        first_name="Admin",
        last_name="User",
        role="admin",
        class_id=school_class.class_id,
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
        seed_classes()
        seed_admin_user()
        print("✅ Seeding abgeschlossen")


if __name__ == "__main__":
    seed()