import uuid
from datetime import datetime
from app.extensions import db

class Chat(db.Model):
    __tablename__ = "chats"

    chat_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(50))
    group_id = db.Column(db.String(36), db.ForeignKey("groups.group_id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)