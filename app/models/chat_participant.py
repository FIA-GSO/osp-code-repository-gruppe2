import uuid
from datetime import datetime
from app.extensions import db

class ChatParticipant(db.Model):
    __tablename__ = "chat_participants"

    chat_participant_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = db.Column(db.String(36), db.ForeignKey("chats.chat_id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    role = db.Column(db.String(50))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)