# ==========================================
# Responsible: Cindy
# Tasks:
# - Test missing required fields
# - Test invalid data types
# - Test empty strings
# - Test invalid category IDs
# - Test overly long input
# - Test invalid request formats
# ==========================================

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


def test_note_requires_title(logged_in_client):
    response = logged_in_client.post("/notes", json={
        "content": "Learn Flask"
    })

    assert response.status_code == 400


def test_note_requires_content(logged_in_client):
    response = logged_in_client.post("/notes", json={
        "title": "Flask"
    })

    assert response.status_code == 400


def test_note_rejects_empty_title(logged_in_client):
    response = logged_in_client.post("/notes", json={
        "title": "",
        "content": "Learn Flask"
    })

    assert response.status_code == 400


def test_note_rejects_title_over_120_characters(logged_in_client):
    response = logged_in_client.post("/notes", json={
        "title": "A" * 121,
        "content": "Learn Flask"
    })

    assert response.status_code == 400


def test_category_requires_name(logged_in_client):
    response = logged_in_client.post("/categories", json={})

    assert response.status_code == 400


def test_category_rejects_empty_name(logged_in_client):
    response = logged_in_client.post("/categories", json={
        "name": ""
    })

    assert response.status_code == 400


def test_category_rejects_name_over_80_characters(logged_in_client):
    response = logged_in_client.post("/categories", json={
        "name": "A" * 81
    })

    assert response.status_code == 400


def test_note_rejects_invalid_category(logged_in_client):
    response = logged_in_client.post("/notes", json={
        "title": "Flask",
        "content": "Learn Flask",
        "category_id": 999
    })

    assert response.status_code == 404