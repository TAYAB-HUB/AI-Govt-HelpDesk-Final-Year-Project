from tests.conftest import login, auth_headers


def test_login_success(client):
    token = login(client, "employee@test.example.com")
    assert token


def test_login_wrong_password_fails(client):
    resp = client.post("/api/auth/login", json={"email": "employee@test.example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_register_and_login_new_user(client):
    resp = client.post("/api/auth/register", json={
        "full_name": "New Person",
        "email": "newperson@test.example.com",
        "password": "Pass@1234",
        "role": "employee",
    })
    assert resp.status_code == 201
    token = login(client, "newperson@test.example.com")
    assert token


def test_register_duplicate_email_fails(client):
    client.post("/api/auth/register", json={
        "full_name": "Dup", "email": "dup@test.example.com", "password": "Pass@1234", "role": "employee",
    })
    resp = client.post("/api/auth/register", json={
        "full_name": "Dup2", "email": "dup@test.example.com", "password": "Pass@1234", "role": "employee",
    })
    assert resp.status_code == 400


def test_me_endpoint_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_endpoint_with_token(client):
    token = login(client, "employee@test.example.com")
    resp = client.get("/api/auth/me", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["email"] == "employee@test.example.com"


def test_employee_cannot_create_department(client):
    token = login(client, "employee@test.example.com")
    resp = client.post(
        "/api/departments",
        json={"name": "New Dept", "code": "NEWD", "description": "x"},
        headers=auth_headers(token),
    )
    assert resp.status_code == 403


def test_super_admin_can_create_department(client):
    token = login(client, "superadmin@test.example.com")
    resp = client.post(
        "/api/departments",
        json={"name": "IT Dept", "code": "ITDEPT", "description": "x"},
        headers=auth_headers(token),
    )
    assert resp.status_code == 201
