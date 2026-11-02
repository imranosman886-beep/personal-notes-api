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


def test_create_category(logged_in_client):
    response = logged_in_client.post("/categories", json={
        "name": "School"
    })

    assert response.status_code == 201
    assert response.json["name"] == "School"


def test_get_categories(logged_in_client):
    logged_in_client.post("/categories", json={
        "name": "School"
    })

    response = logged_in_client.get("/categories")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_single_category(logged_in_client):
    create_response = logged_in_client.post("/categories", json={
        "name": "Personal"
    })

    category_id = create_response.json["id"]

    response = logged_in_client.get(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json["name"] == "Personal"


def test_update_category(logged_in_client):
    create_response = logged_in_client.post("/categories", json={
        "name": "School"
    })

    category_id = create_response.json["id"]

    response = logged_in_client.patch(
        f"/categories/{category_id}",
        json={"name": "Work"}
    )

    assert response.status_code == 200
    assert response.json["name"] == "Work"


def test_delete_category(logged_in_client):
    create_response = logged_in_client.post("/categories", json={
        "name": "School"
    })

    category_id = create_response.json["id"]

    response = logged_in_client.delete(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json == {}

    response = logged_in_client.get(f"/categories/{category_id}")
    assert response.status_code == 404


def test_cannot_access_categories_without_login(client):
    response = client.get("/categories")

    assert response.status_code == 401


def test_cannot_access_another_users_category(logged_in_client):
    create_response = logged_in_client.post("/categories", json={
        "name": "Private"
    })

    category_id = create_response.json["id"]

    logged_in_client.delete("/logout")

    logged_in_client.post("/signup", json={
        "username": "john",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = logged_in_client.get(f"/categories/{category_id}")

    assert response.status_code == 404


def test_delete_category_removes_note_assignment(logged_in_client):
    category_response = logged_in_client.post("/categories", json={
        "name": "School"
    })

    category_id = category_response.json["id"]

    note_response = logged_in_client.post("/notes", json={
        "title": "Revision",
        "content": "Study Flask",
        "category_id": category_id
    })

    note_id = note_response.json["id"]

    logged_in_client.delete(f"/categories/{category_id}")

    response = logged_in_client.get(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.json["category_id"] is None