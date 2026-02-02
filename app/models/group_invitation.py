import uuid
from datetime import datetime
from app.extensions import db

class GroupInvitation(db.Model):
    __tablename__ = "group_invitations"

    group_invitation_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = db.Column(db.String(36), db.ForeignKey("groups.group_id"), nullable=False)
    invited_user = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)
    invited_by = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    status = db.Column(db.String(50))
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)