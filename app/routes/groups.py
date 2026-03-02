from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.group import Group
from app.extensions import db
from flask import redirect, url_for

import uuid

print("IMPORT groups.py:", __file__)
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

@groups_bp.route("/my_teams")
@login_required
def my_teams():
    groups = (
        Group.query
        .filter(Group.deleted_at.is_(None))
        .order_by(Group.created_at.desc())
        .all()
    )

    return render_template(
        "overview/html/my_teams.html",
        user=current_user,
        groups=groups
    )



@groups_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_group():
    if request.method == "GET":
        return render_template("createGroup/html/create_group.html", user=current_user)

    # Formdaten holen
    name = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip() or None
    join_policy = (request.form.get("join_policy") or "open").strip()
    max_members_raw = (request.form.get("max_members") or "").strip()
    is_cross_class = bool(request.form.get("is_cross_class"))  # optional

    # Validierung
    errors = []
    if not name:
        errors.append("Gruppenname ist erforderlich.")
    if join_policy not in {"open", "invite", "closed"}:
        errors.append("Ungültige Beitrittsart.")

    try:
        max_members = int(max_members_raw)
        if max_members < 1:
            errors.append("Max. Mitglieder muss mindestens 1 sein.")
    except ValueError:
        errors.append("Max. Mitglieder muss eine Zahl sein.")
        max_members = None

    if errors:
        for e in errors:
            flash(e, "error")
        return render_template(
            "createGroup/html/create_group.html",
            user=current_user,
            form={
                "name": name,
                "description": description or "",
                "join_policy": join_policy,
                "max_members": max_members_raw,
                "is_cross_class": is_cross_class
            }
        ), 422

    # ✅ Gruppe erstellen – leader_id MUSS gesetzt werden
    group = Group(
        group_id=str(uuid.uuid4()),     # falls dein Model das nicht automatisch macht
        name=name,
        description=description,
        max_members=max_members,
        join_policy=join_policy,
        leader_id=current_user.user_id if hasattr(current_user, "user_id") else current_user.id,
        is_cross_class=is_cross_class
    )

    db.session.add(group)
    db.session.commit()

    flash("Gruppe wurde erstellt!", "success")
    return redirect(url_for("groups.my_teams"))
