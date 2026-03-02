from app.routes.groups import Group
import uuid

def test_list_groups(client, test_group):
    """Testet, ob die Listenansicht lädt und die Testgruppe enthält."""
    response = client.get("/groups/")

    assert response.status_code == 200
    # Prüft, ob der Name der Gruppe im gerenderten HTML vorkommt
    assert b"Test Gruppe" in response.data

def test_new_group_form(client):
    """Testet, ob das Formular zum Erstellen einer Gruppe geladen wird."""
    response = client.get("/groups/new")
    assert response.status_code == 200

def test_create_group_success(client, test_user):
    """Testet das erfolgreiche Erstellen einer Gruppe via POST."""

    # 1. Wir machen aus den User-Bytes einen String für das HTML-Formular
    leader_id_string = str(uuid.UUID(bytes=test_user.user_id))

    data = {
        "name": "Neue Pytest Gruppe",
        "description": "Eine Gruppe für Tests",
        "leader_id": leader_id_string,  # <-- Hier übergeben wir jetzt den String!
        "join_policy": "invite",
    }

    response = client.post("/groups/new", data=data)

    assert response.status_code == 302
    assert "/groups" in response.headers["Location"]

    group_in_db = Group.query.filter_by(name="Neue Pytest Gruppe").first()
    assert group_in_db is not None
    # Hier prüfen wir auch gegen den String!
    assert group_in_db.leader_id == leader_id_string

def test_create_group_missing_name(client, test_user):
    """Testet die Validierung, wenn der Name fehlt."""
    data = {
        "name": "", # Name fehlt absichtlich
        "leader_id": test_user.user_id
    }

    response = client.post("/groups/new", data=data)

    # Die Route gibt 400 Bad Request zurück, wenn Fehler auftreten
    assert response.status_code == 400
    assert b"Name ist erforderlich." in response.data

def test_show_group(client, test_group):
    """Testet die Detailansicht einer Gruppe."""
    response = client.get(f"/groups/{test_group.group_id}")

    # Hier gehört dieser Check hin (nur Status prüfen)
    assert response.status_code == 200

def test_update_group(client, test_group):
    """Testet das Aktualisieren einer bestehenden Gruppe."""
    data = {
        "name": "Aktualisierter Gruppenname",
        "join_policy": "open"
    }

    response = client.post(f"/groups/{test_group.group_id}/edit", data=data)

    assert response.status_code == 302

    # DB prüfen, ob sich der Name geändert hat
    updated_group = Group.query.get(test_group.group_id)
    assert updated_group.name == "Aktualisierter Gruppenname"
    assert updated_group.join_policy == "open"

def test_delete_group(client, test_group):
    """Testet das Löschen einer Gruppe."""
    group_id = test_group.group_id

    response = client.post(f"/groups/{group_id}/delete")

    assert response.status_code == 302

    # Prüfen, ob die Gruppe aus der DB gelöscht wurde
    deleted_group = Group.query.get(group_id)
    assert deleted_group is None