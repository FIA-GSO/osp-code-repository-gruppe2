import uuid
from datetime import datetime
from app.extensions import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    audit_log_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    action = db.Column(db.Text, nullable=False)
    target_type = db.Column(db.Text, nullable=False)
    target_id = db.Column(db.String(36))
    payload = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
