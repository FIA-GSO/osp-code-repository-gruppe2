# app/models/school_class.py
from datetime import datetime, UTC
from app.extensions import db

class SchoolClass(db.Model):
    __tablename__ = "school_classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # z.B. "FI-23A"
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    # optional: Rückbeziehung zu User
    users = db.relationship("User", back_populates="school_class", lazy=True)

    def __repr__(self):
        return f"<SchoolClass {self.name}>"