from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import uuid

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login_form"


@login_manager.user_loader
def load_user(user_id: str):
    """
    user_id kommt als STRING (hex) aus der Session
    In der DB ist es UUID als BLOB (bytes)
    """
    try:
        from app.models.user import User  # LAZY IMPORT – extrem wichtig
        return User.query.get(uuid.UUID(user_id).bytes)
    except Exception:
        return None