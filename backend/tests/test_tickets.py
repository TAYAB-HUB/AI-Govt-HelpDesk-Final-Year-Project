from tests.conftest import login, auth_headers


def _get_hr_department_id(client, token):
    resp = client.get("/api/departments", headers=auth_headers(token))
    for d in resp.json():
        if d["code"] == "HR":
            return d["id"]
    raise AssertionError("HR department not found")


def test_employee_can_create_ticket(client):
    token = login(client, "employee@test.example.com")
    dept_id = _get_hr_department_id(client, token)
    resp = client.post("/api/tickets", json={
        "department_id": dept_id,
        "category": "HR - Leave",
        "subject": "Leave query",
        "description": "How much leave do I have left?",
        "priority": "medium",
    }, headers=auth_headers(token))
    assert resp.status_code == 201
    assert resp.json()["status"] == "open"


def test_employee_cannot_create_ticket_for_other_department(client):
    token = login(client, "employee@test.example.com")  # belongs to HR
    resp = client.post("/api/tickets", json={
        "department_id": 999999,
        "category": "Other",
        "subject": "x",
        "description": "x",
    }, headers=auth_headers(token))
    assert resp.status_code in (403, 404)


def test_employee_only_sees_own_tickets(client):
    emp_token = login(client, "employee@test.example.com")
    other_token = login(client, "fin.employee@test.example.com")

    resp = client.get("/api/tickets", headers=auth_headers(other_token))
    assert resp.status_code == 200
    # the finance employee shouldn't see the HR employee's ticket from the previous test
    subjects = [t["subject"] for t in resp.json()]
    assert "Leave query" not in subjects


def test_employee_cannot_change_ticket_status(client):
    token = login(client, "employee@test.example.com")
    dept_id = _get_hr_department_id(client, token)
    ticket = client.post("/api/tickets", json={
        "department_id": dept_id, "category": "HR - Leave", "subject": "t2", "description": "d",
    }, headers=auth_headers(token)).json()

    resp = client.post(f"/api/tickets/{ticket['id']}/comments", json={
        "body": "trying to close my own ticket",
        "status_change_to": "closed",
    }, headers=auth_headers(token))
    assert resp.status_code == 403


def test_officer_can_change_ticket_status(client):
    emp_token = login(client, "employee@test.example.com")
    officer_token = login(client, "officer@test.example.com")
    dept_id = _get_hr_department_id(client, emp_token)

    ticket = client.post("/api/tickets", json={
        "department_id": dept_id, "category": "HR - Leave", "subject": "t3", "description": "d",
    }, headers=auth_headers(emp_token)).json()

    resp = client.post(f"/api/tickets/{ticket['id']}/comments", json={
        "body": "Looking into it",
        "status_change_to": "in_progress",
    }, headers=auth_headers(officer_token))
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"
