import os
from flask import Flask
from app.extensions import db, migrate
from config import Config

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.abspath(
        os.path.join(base_dir, "..", "frontend", "templates")
    )

    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(Config)

    # DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Modelle (für Alembic / Mapper)
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

    # Blueprint
    from app.routes.groups import groups_bp
    app.register_blueprint(groups_bp)

    # ✅ RICHTIGES DEBUGGING
    print("🔎 Flask template_folder:", app.template_folder)
    print("🔎 Template folder exists:", os.path.exists(app.template_folder))

    return app