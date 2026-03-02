import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.group import Group
from app.models.user import User

from flask import Blueprint, render_template
from flask_login import login_required, current_user

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")

def _now():
    return datetime.utcnow()

def _uuid_str():
    return str(uuid.uuid4())

def _parse_leader_id(leader_id_str: str):
    if not leader_id_str:
        return None
    s = leader_id_str.strip()
    if len(s) == 32:  # hex → bytes (falls user_id als BLOB gespeichert)
        try:
            return bytes.fromhex(s)
        except ValueError:
            return s
    return s  # 36-Zeichen-UUID (String) oder anderes

# READ (Liste)
@groups_bp.route("/", methods=["GET"], strict_slashes=False)
def list_groups():
    groups = Group.query.order_by(Group.created_at.desc().nullslast()).all()
    return render_template("groups_list.html", groups=groups)

# CREATE (Form)
@groups_bp.route("/new", methods=["GET"], strict_slashes=False)
def new_group_form():
    users = User.query.filter_by(is_active=True).order_by(User.first_name, User.last_name).all()
    return render_template("groups_create.html", users=users)

# CREATE (Submit)
@groups_bp.route("/new", methods=["POST"])
def create_group():
    name        = request.form.get("name", "").strip()
    description = request.form.get("description") or ""
    max_members = request.form.get("max_members") or None
    join_policy = request.form.get("join_policy") or "open"
    leader_id_str = request.form.get("leader_id") or ""

    errors = []
    if not name:
        errors.append("Gruppenname ist erforderlich.")
    if not leader_id_str:
        errors.append("Leiter:in ist erforderlich.")

    try:
        max_members = int(max_members) if max_members not in (None, "") else None
        if max_members is not None and max_members < 2:
            errors.append("Max. Mitglieder muss mindestens 2 sein.")
    except ValueError:
        errors.append("Max. Mitglieder muss eine Zahl sein.")

    if not max_members:
        errors.append("Max. Mitglieder ist erforderlich.")

    if errors:
        for e in errors:
            flash(e, "error")
        users = User.query.filter_by(is_active=True).order_by(User.first_name, User.last_name).all()
        return render_template("groups_create.html", users=users, form=request.form), 400

    leader_id = _parse_leader_id(leader_id_str)

    group = Group(
        group_id=_uuid_str(),
        name=name,
        description=description,
        max_members=max_members,
        join_policy=join_policy,
        leader_id=leader_id,
        created_at=_now(),
        updated_at=_now(),
    )

    try:
        db.session.add(group)
        db.session.commit()
        flash("Gruppe wurde erstellt.", "success")
        return redirect(url_for("groups.list_groups"))
    except SQLAlchemyError as exc:
        db.session.rollback()
        flash(f"Fehler beim Speichern: {exc}", "error")
        users = User.query.filter_by(is_active=True).order_by(User.first_name, User.last_name).all()
        return render_template("groups_create.html", users=users, form=request.form), 500


@groups_bp.route("/<group_id>", methods=["GET"])
def show_group(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template("groups_show.html", group=group)


@groups_bp.route("/<group_id>/edit", methods=["GET"])
def edit_group_form(group_id):
    group = Group.query.get_or_404(group_id)
    users = User.query.filter_by(is_active=True).order_by(
        User.first_name, User.last_name
    ).all()
    return render_template("groups_edit.html", group=group, users=users)


@groups_bp.route("/<group_id>/edit", methods=["POST"])
def update_group(group_id):
    group = Group.query.get_or_404(group_id)

    group.name        = request.form.get("name", "").strip()
    group.description = request.form.get("description") or None
    group.max_members = request.form.get("max_members") or None
    group.join_policy = request.form.get("join_policy")
    group.updated_at  = _now()

    try:
        db.session.commit()
        flash("Gruppe wurde aktualisiert.", "success")
        return redirect(url_for("groups.list_groups"))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Fehler beim Aktualisieren: {e}", "error")
        return redirect(url_for("groups.edit_group_form", group_id=group.group_id))


@groups_bp.route("/<group_id>/delete", methods=["POST"])
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)

    try:
        db.session.delete(group)
        db.session.commit()
        flash("Gruppe wurde gelöscht.", "success")
        return redirect(url_for("groups.list_groups"))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Löschen fehlgeschlagen: {e}", "error")
        return redirect(url_for("groups.show_group", group_id=group.group_id))

@groups_bp.route("/api", methods=["GET"])
def get_groups_json():
    groups = Group.query.order_by(Group.created_at.desc()).all()
    return jsonify([{
        "group_id":    g.group_id,
        "name":        g.name,
        "description": g.description or "",
        "max_members": g.max_members,
        "join_policy": g.join_policy,
    } for g in groups])

@groups_bp.route("/")
@login_required
def group_list():
    return render_template("group/html/groups_list.html", user=current_user)