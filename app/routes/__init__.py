import os
from flask import Flask
from app.extensions import db

def create_app(test_config=None):
    """Die Application Factory für Flask."""

    # Pfad zu deinen Templates (wie in deinem vorherigen Code)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.abspath(
        os.path.join(base_dir, "..", "frontend", "templates")
    )

    app = Flask(__name__, template_folder=template_dir)

    # Basis-Konfiguration
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Test-Konfiguration überschreiben (wird von der conftest.py genutzt)
    if test_config is not None:
        app.config.update(test_config)

    # Datenbank an die App binden
    db.init_app(app)

    # ==========================================
    # 1. ALLE MODELLE IMPORTIEREN
    # Wichtig: SchoolClass muss VOR User geladen werden!
    # ==========================================
    from app.models.school_class import SchoolClass
    from app.models.user import User
    from app.models.group import Group
    from app.models.tag import Tag
    from app.models.group_tag import GroupTag
    from app.models.group_member import GroupMember
    from app.models.group_invitation import GroupInvitation
    from app.models.chat import Chat
    from app.models.chat_participant import ChatParticipant
    from app.models.chat_message import ChatMessage
    from app.models.user_consent import UserConsent
    from app.models.audit_log import AuditLog
    from app.models.report import Report

    # ==========================================
    # 2. BLUEPRINTS (ROUTEN) REGISTRIEREN
    # ==========================================
    from app.routes.groups import groups_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(groups_bp)
    app.register_blueprint(auth_bp)

    return app