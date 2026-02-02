import uuid
from datetime import datetime
from app.extensions import db

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    chat_message_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = db.Column(db.String(36), db.ForeignKey("chats.chat_id"), nullable=False)
    sender_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    edited_at = db.Column(db.DateTime)

    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.String(36), db.ForeignKey("users.user_id"))

    is_flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.Text)