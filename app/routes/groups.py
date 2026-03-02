from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


@groups_bp.route("/")
@login_required
def group_list():
    return render_template("overview/html/my_teams.html", user=current_user)


@groups_bp.route("/explore")
@login_required
def explore():
    return render_template("overview/html/erkunden.html", user=current_user)


@groups_bp.route("/create", methods=["GET"])
@login_required
def create_group_form():
    return render_template("createGroup/html/create-group.html", user=current_user)


@groups_bp.route("/new", methods=["POST"])
@login_required
def create_group():
    name        = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    max_members = request.form.get("max_members")
    join_policy = request.form.get("join_policy", "open")

    if not name:
        return jsonify({"ok": False, "error": "Name fehlt"}), 422

    # TODO: Gruppe in DB speichern

    return redirect(url_for("groups.group_list"))