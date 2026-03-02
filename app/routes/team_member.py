from flask import Blueprint, render_template
from flask_login import login_required, current_user

from flask import render_template
from sqlalchemy import cast, String
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User
from app.extensions import db


groups_m = Blueprint("groups", __name__, url_prefix="/groups")



@groups_m.route("/groups/<string:group_id>/members")
###@login_required

def show_group_members(group_id):
    
    group = Group.query.filter_by(group_id=group_id).first_or_404()

    members = (
        db.session.query(User)
        .join(
            GroupMember,
            cast(User.user_id, String) == GroupMember.user_id
        )
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    return render_template(
        "teamview-teammembers/html/Team_Team_member.html",group=group,
        members=members    )