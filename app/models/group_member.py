import uuid
from datetime import datetime
from app.extensions import db

class GroupMember(db.Model):
    __tablename__ = "group_members"

    group_member_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = db.Column(db.String(36), db.ForeignKey("groups.group_id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    role = db.Column(db.String(50))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint("group_id", "user_id"),
    )