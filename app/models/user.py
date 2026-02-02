import uuid
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    # PK
    user_id = db.Column(
        BLOB,
        primary_key=True,
        default=lambda: uuid.uuid4().bytes
    )

    # Pflichtfelder
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    # Optional
    role = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    last_login_at = db.Column(db.DateTime)
