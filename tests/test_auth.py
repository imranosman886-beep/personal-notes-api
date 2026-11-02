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


def test_signup(client):
    response = client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "password123"
    })

    assert response.status_code == 201
    assert response.json["username"] == "imran"


def test_signup_rejects_short_password(client):
    response = client.post("/signup", json={
        "username": "imran",
        "password": "123",
        "password_confirmation": "123"
    })

    assert response.status_code == 400


def test_signup_rejects_password_mismatch(client):
    response = client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "different123"
    })

    assert response.status_code == 400


def test_signup_rejects_missing_fields(client):
    response = client.post("/signup", json={
        "username": "imran"
    })

    assert response.status_code == 400


def test_login(client):
    client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "password123"
    })

    client.delete("/logout")

    response = client.post("/login", json={
        "username": "imran",
        "password": "password123"
    })

    assert response.status_code == 200
    assert response.json["username"] == "imran"


def test_login_with_wrong_password(client):
    client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "password123"
    })

    client.delete("/logout")

    response = client.post("/login", json={
        "username": "imran",
        "password": "wrongpassword"
    })

    assert response.status_code == 401


def test_login_rejects_missing_fields(client):
    response = client.post("/login", json={
        "username": "imran"
    })

    assert response.status_code == 400


def test_check_session(client):
    client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = client.get("/check_session")

    assert response.status_code == 200
    assert response.json["username"] == "imran"


def test_logout(client):
    client.post("/signup", json={
        "username": "imran",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = client.delete("/logout")

    assert response.status_code == 200
    assert response.json == {}

    response = client.get("/check_session")
    assert response.json == {}