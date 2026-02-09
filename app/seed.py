
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.tag import Tag
from app.models.group import Group
from app.models.group_member import GroupMember

def uuid_str():
    return str(uuid.uuid4())

def seed():
    app = create_app()
    with app.app_context():

        # ---------- USERS ----------
        admin_id = uuid.uuid4().bytes
        user_id = uuid.uuid4().bytes

        admin = User(
            user_id=admin_id,
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role="admin",
            is_active=True,
            created_at=datetime.utcnow()
        )

        user = User(
            user_id=user_id,
            email="user@example.com",
            password=generate_password_hash("user123"),
            first_name="Normal",
            last_name="User",
            role="user",
            is_active=True,
            created_at=datetime.utcnow()
        )

        db.session.add_all([admin, user])
        db.session.flush()

        # ---------- TAGS ----------
        tags = [
            Tag(tag_id=uuid_str(), name="Sport", is_predefined=True),
            Tag(tag_id=uuid_str(), name="Programmieren", is_predefined=True),
            Tag(tag_id=uuid_str(), name="Gaming", is_predefined=True),
        ]
        db.session.add_all(tags)

        # ---------- GROUP ----------
        group_id = uuid_str()

        group = Group(
            group_id=group_id,
            name="Flask Entwickler",
            description="Gruppe für Flask & Python",
            min_members=1,
            max_members=10,
            join_policy="invite",
            leader_id=admin_id,
            is_cross_class=False,
            created_at=datetime.utcnow()
        )

        db.session.add(group)
        db.session.flush()

        # ---------- GROUP MEMBERS ----------
        members = [
            GroupMember(
                group_member_id=uuid_str(),
                group_id=group_id,
                user_id=admin_id,
                role="leader",
                joined_at=datetime.utcnow()
            ),
            GroupMember(
                group_member_id=uuid_str(),
                group_id=group_id,
                user_id=user_id,
                role="member",
                joined_at=datetime.utcnow()
            )
        ]

        db.session.add_all(members)

        db.session.commit()
        print("✅ Seed erfolgreich ausgeführt")

if __name__ == "__main__":
    seed()