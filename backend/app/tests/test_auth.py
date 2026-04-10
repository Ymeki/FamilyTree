# FILE: /FamilyTree/FamilyTree/backend/app/tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.services.auth_service import create_user, authenticate_user
from app.schemas.pydantic_models import UserCreate

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user():
    user_data = UserCreate(username="testuser", email="test@example.com", password="password")
    create_user(user_data)
    return user_data

def test_register(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

def test_login(client, test_user):
    response = client.post("/api/v1/auth/login", data={
        "username": test_user.username,
        "password": "password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", data={
        "username": "invaliduser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"