from flask import Blueprint, render_template
from flask_login import login_required, current_user

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")

@groups_bp.route("/")
@login_required
def group_list():
    return render_template("overview/html/erkunden.html", user=current_user)

