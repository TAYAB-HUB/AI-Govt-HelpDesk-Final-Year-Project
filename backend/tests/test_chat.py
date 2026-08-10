import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    response = client.post("/auth/login", json={
        "email": "employee@demo.gov.in",
        "password": "employee123"
    })
    return response.json()["access_token"]

def test_ask_question(auth_token):
    response = client.post(
        "/chat/ask",
        json={
            "question": "What is the leave policy?",
            "department_id": 1
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data