# app/models/group.py
import uuid
from datetime import datetime
from app.extensions import db

class Group(db.Model):
    __tablename__ = "groups"  # WICHTIG: nicht 'group' (reserved keyword)

    group_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    min_members = db.Column(db.Integer)
    max_members = db.Column(db.Integer)
    join_policy = db.Column(db.String(50))

    leader_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    is_cross_class = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity_at = db.Column(db.DateTime)
    # In deinem Sheet stand 'deleted_at_' – ich habe das als 'deleted_at' vereinheitlicht.
    # Wenn ihr explizit 'deleted_at_' wollt, benenne die Spalte unten entsprechend um.
    deleted_at = db.Column(db.DateTime)

    # am Ende der Group-Klasse einfach hinzufügen
def to_dict(self):
    return {
        "id":          self.group_id,
        "name":        self.name,
        "description": self.description,
        "max_members": self.max_members,
        "join_policy": self.join_policy,
        "leader_id":   self.leader_id,
    }