from flask import Flask
from app.extensions import db, migrate
from config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Modelle importieren (WICHTIG für Migrationen)
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

    @app.route("/")
    def index():
        return "Lerngruppentool läuft ✅"

    return app