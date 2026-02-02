import uuid
from datetime import datetime
from app.extensions import db

class Report(db.Model):
    __tablename__ = "reports"

    report_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reporter_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    target_type = db.Column(db.String(50))
    target_id = db.Column(db.String(36))

    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.String(36), db.ForeignKey("users.user_id"))
