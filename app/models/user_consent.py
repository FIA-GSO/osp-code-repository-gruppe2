import uuid
from datetime import datetime
from app.extensions import db

class UserConsent(db.Model):
    __tablename__ = "user_consents"

    user_consent_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    policy_version = db.Column(db.Text, nullable=False)
    consented_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    withdrawn_at = db.Column(db.DateTime)