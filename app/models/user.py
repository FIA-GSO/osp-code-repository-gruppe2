import uuid
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        BLOB,
        primary_key=True,
        default=lambda: uuid.uuid4().bytes
    )

    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    last_login_at = db.Column(db.DateTime)

    
# NEW: Klassenbezug
    school_class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=True)
    school_class = db.relationship("SchoolClass", back_populates="users")


    def get_id(self) -> str:
        return uuid.UUID(bytes=self.user_id).hex