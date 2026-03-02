import os
from flask import Flask, redirect, url_for, render_template
from flask_cors import CORS
from app.extensions import db, migrate, login_manager
from config import Config

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "..", "frontend", "pages"),
        static_folder=os.path.join(base_dir, "..", "frontend", "pages"),
        static_url_path=""
    )

    app.config.from_object(Config)
    CORS(app)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_form"

    # Modelle
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
    from app.models.school_class import SchoolClass

    # Blueprints
    from app.routes.groups import groups_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(groups_bp)
    app.register_blueprint(auth_bp)

    # Root → Login
    @app.route("/")
    def index():
        return redirect(url_for("auth.login_form"))

    @app.errorhandler(401)
    def unauthorized(e):
        return redirect(url_for("auth.login_form"))

    @app.errorhandler(404)
    def not_found(e):
        # return render_template("404.html"), 404
        return "Seite nicht gefunden.", 404

    return app