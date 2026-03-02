from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.group import Group

from flask import redirect, url_for


groups_bp = Blueprint("groups", __name__, url_prefix="/groups")



@groups_bp.route("/")
@login_required
def groups_root_redirect():
    return redirect(url_for("groups.explore"))



@groups_bp.route("/explore")
@login_required
def explore():
    groups = (
        Group.query
        .filter(Group.deleted_at.is_(None))
        .order_by(Group.created_at.desc())
        .all()
    )

    return render_template(
        "overview/html/erkunden.html",
        user=current_user,
        groups=groups
    )