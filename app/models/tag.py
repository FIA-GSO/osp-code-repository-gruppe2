import uuid
from app.extensions import db

class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.Text, nullable=False, unique=True)
    is_predefined = db.Column(db.Boolean, default=False)