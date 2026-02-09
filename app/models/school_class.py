import uuid
from datetime import datetime
from app.extensions import db

class SchoolClass(db.Model):
    __tablename__ = "school_classes"

    class_id = db.Column(db.String(36), primary_key=True,default=lambda: str(uuid.uuid4()))
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)