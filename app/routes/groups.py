from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.group import Group

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


# ── Seiten ────────────────────────────────────────────────────────────────────

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


# ── Gruppe erstellen ──────────────────────────────────────────────────────────

@groups_bp.route("/new", methods=["POST"])
@login_required
def create_group():
    name        = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    join_policy = request.form.get("join_policy", "open")

    try:
        max_members = int(request.form.get("max_members", 10))
        if max_members < 1:
            raise ValueError
    except ValueError:
        return jsonify({"ok": False, "error": "Ungültige Mitgliederzahl"}), 422

    if not name:
        return jsonify({"ok": False, "error": "Name fehlt"}), 422

    gruppe = Group(
        name        = name,
        description = description or None,
        max_members = max_members,
        join_policy = join_policy,
        leader_id   = current_user.user_id,
    )

    db.session.add(gruppe)
    db.session.commit()

    return redirect(url_for("groups.group_list"))


# ── API ───────────────────────────────────────────────────────────────────────

@groups_bp.route("/api/mine")
@login_required
def api_mine():
    """Gruppen, die der eingeloggte User erstellt hat."""
    gruppen = Group.query.filter_by(
        leader_id  = current_user.user_id,
        deleted_at = None
    ).all()
    return jsonify([g.to_dict() for g in gruppen])


@groups_bp.route("/api/explore")
@login_required
def api_explore():
    """Alle anderen Gruppen (nicht vom eingelogsten User)."""
    gruppen = Group.query.filter(
        Group.leader_id  != current_user.user_id,
        Group.deleted_at == None
    ).all()
    return jsonify([g.to_dict() for g in gruppen])