import uuid
from datetime import datetime, UTC
from werkzeug.security import generate_password_hash

import os

from app import create_app
from app.extensions import db
from app.models.group import Group  
from app.models.user import User
from app.models.school_class import SchoolClass


def _user_id_to_leader_id(user_id_value):
    """
    Konvertiert User.user_id (bei dir BLOB/bytes) in ein Format,
    das in Group.leader_id passt.
    - wenn bytes -> UUID string
    - wenn schon string -> 그대로
    """
    if user_id_value is None:
        return None

    # Falls es bytes ist (BLOB): UUID daraus machen => "xxxxxxxx-xxxx-...."
    if isinstance(user_id_value, (bytes, bytearray)):
        return str(uuid.UUID(bytes=user_id_value))

    # Falls es bereits ein String ist:
    return str(user_id_value)


def seed_groups():
    """
    Erstellt 3 Dummy-Gruppen, falls noch nicht vorhanden.
    leader_id wird auf den seeded User/`max.mustermann` gesetzt, falls vorhanden,
    ansonsten auf den Admin.
    """

    # 1) Leader bestimmen (erst max.mustermann, sonst admin)
    leader_user = User.query.filter_by(email="max.mustermann@gso.schule.koeln").first()
    if not leader_user:
        leader_user = User.query.filter_by(email="admin@example.com").first()

    if not leader_user:
        print("❌ Kein Leader-User gefunden – erst seed_users/seed_admin_user ausführen.")
        return

    leader_id_value = _user_id_to_leader_id(leader_user.user_id)

    dummy_groups = [
        {
            "name": "Mathe-Lernrunde FI101",
            "description": "Wir üben Analysis & Algebra – Fokus auf Klausurvorbereitung.",
            "min_members": 2,
            "max_members": 8,
            "join_policy": "open",     # frei beitreten
            "is_cross_class": False,
        },
        {
            "name": "Python Projektgruppe",
            "description": "Gemeinsam kleine Apps bauen, Code Reviews, Git-Workflow.",
            "min_members": 3,
            "max_members": 12,
            "join_policy": "invite",   # nur per Einladung / Anfrage
            "is_cross_class": True,
        },
        {
            "name": "Datenbanken & SQL",
            "description": "ER-Modell, Normalformen, SQL Queries – gegenseitige Hilfe.",
            "min_members": 2,
            "max_members": 10,
            "join_policy": "closed",   # geschlossen
            "is_cross_class": True,
        },
    ]

    created = 0
    skipped = 0

    for g in dummy_groups:
        # Duplikate vermeiden über Namen
        if Group.query.filter_by(name=g["name"]).first():
            skipped += 1
            continue

        group = Group(
            name=g["name"],
            description=g["description"],
            min_members=g["min_members"],
            max_members=g["max_members"],
            join_policy=g["join_policy"],
            leader_id=leader_id_value,
            is_cross_class=g["is_cross_class"],
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            last_activity_at=datetime.now(UTC),
        )
        db.session.add(group)
        created += 1

    db.session.commit()
    print(f"✅ Dummy-Gruppen: {created} erstellt, {skipped} übersprungen")

def seed_users():
    """Erstellt einen Admin-User, falls er noch nicht existiert"""
    user_email = "max.mustermann@gso.schule.koeln"

    if User.query.filter_by(email=user_email).first():
        print("⚠️ User existiert bereits – übersprungen")
        return

    user = User(
        user_id=uuid.uuid4().bytes,
        email=user_email,
        password=generate_password_hash("Test1234!"),
        first_name="Max",
        last_name="Mustermann",
        role="user",
        is_active=True,
        created_at=datetime.now(UTC)
    )

    db.session.add(user)
    db.session.commit()
    print("✅ Admin-User erstellt (max.mustermann@gso.schule.koeln)")


def seed_school_classes():
    """Erstellt Klassen nach Muster FI<1-3>0<1-3> => FI101..FI303"""
    created = 0
    skipped = 0

    for grade in range(1, 4):          # 1..3
        for group in range(1, 4):      # 1..3
            name = f"FI{grade}0{group}"  # FI101, FI102, ...
            if SchoolClass.query.filter_by(name=name).first():
                skipped += 1
                continue

            db.session.add(SchoolClass(name=name))
            created += 1

    db.session.commit()
    print(f"✅ Schulklassen: {created} erstellt, {skipped} übersprungen")

def seed_admin_user():
    """Erstellt einen Admin-User, falls er noch nicht existiert"""
    admin_email = "admin@example.com"

    if User.query.filter_by(email=admin_email).first():
        print("⚠️ Admin-User existiert bereits – übersprungen")
        return

    admin = User(
        user_id=uuid.uuid4().bytes,
        email=admin_email,
        password=generate_password_hash("Admin1234!"),
        first_name="Admin",
        last_name="User",
        role="admin",
        is_active=True,
        created_at=datetime.now(UTC)
    )

    db.session.add(admin)
    db.session.commit()
    print("✅ Admin-User erstellt (admin@example.com)")


def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding gestartet...")
        seed_admin_user()
        seed_users()
        seed_school_classes()
        seed_groups()
        print("✅ Seeding abgeschlossen")


if __name__ == "__main__":
    seed()