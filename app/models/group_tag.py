import uuid
from app.extensions import db

class GroupTag(db.Model):
    __tablename__ = "group_tags"

    group_tag_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = db.Column(db.String(36), db.ForeignKey("groups.group_id"), nullable=False)
    tag_id = db.Column(db.String(36), db.ForeignKey("tags.tag_id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("group_id", "tag_id"),
    )