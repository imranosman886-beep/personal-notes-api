import pytest

from app import create_app
from models import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()


@pytest.fixture
def logged_in_client(client):
    client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "password123"
    })

    return client


def test_create_note(logged_in_client):
    response = logged_in_client.post("/notes", json={
        "title": "Flask",
        "content": "Learn Flask routes"
    })

    assert response.status_code == 201
    assert response.json["title"] == "Flask"


def test_get_notes(logged_in_client):
    logged_in_client.post("/notes", json={
        "title": "Flask",
        "content": "Learn Flask"
    })

    response = logged_in_client.get("/notes")

    assert response.status_code == 200
    assert len(response.json["notes"]) == 1


def test_get_single_note(logged_in_client):
    create_response = logged_in_client.post("/notes", json={
        "title": "SQL",
        "content": "Learn SQLAlchemy"
    })

    note_id = create_response.json["id"]

    response = logged_in_client.get(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.json["title"] == "SQL"


def test_update_note(logged_in_client):
    create_response = logged_in_client.post("/notes", json={
        "title": "Old title",
        "content": "Some content"
    })

    note_id = create_response.json["id"]

    response = logged_in_client.patch(f"/notes/{note_id}", json={
        "title": "New title"
    })

    assert response.status_code == 200
    assert response.json["title"] == "New title"


def test_delete_note(logged_in_client):
    create_response = logged_in_client.post("/notes", json={
        "title": "To delete",
        "content": "Some content"
    })

    note_id = create_response.json["id"]

    response = logged_in_client.delete(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.json == {}

    response = logged_in_client.get(f"/notes/{note_id}")
    assert response.status_code == 404


def test_cannot_access_notes_without_login(client):
    response = client.get("/notes")

    assert response.status_code == 401


def test_cannot_access_another_users_note(logged_in_client):
    create_response = logged_in_client.post("/notes", json={
        "title": "Private note",
        "content": "Only Imran should see this"
    })

    note_id = create_response.json["id"]

    logged_in_client.delete("/logout")

    logged_in_client.post("/signup", json={
        "username": "john",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = logged_in_client.get(f"/notes/{note_id}")

    assert response.status_code == 404

# ==========================================
# Responsible: Abdimajid
# File: test_notes.py
# Tasks:
# - Test retrieving notes
# - Test creating notes
# - Test updating notes
# - Test deleting notes
# - Test access restrictions between users
# - Test pagination
# - Test invalid note data
# ==========================================