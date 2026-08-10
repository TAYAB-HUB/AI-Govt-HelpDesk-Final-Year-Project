import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "test@demo.gov.in",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "Employee",
        "department_id": 1
    })
    assert response.status_code in [201, 400]  # 400 if already exists

def test_login():
    response = client.post("/auth/login", json={
        "email": "employee@demo.gov.in",
        "password": "employee123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid():
    response = client.post("/auth/login", json={
        "email": "wrong@demo.gov.in",
        "password": "wrongpass"
    })
    assert response.status_code == 401