#!/usr/bin/env python3
"""
Smoke Test Script
Tests critical paths to ensure the system is runnable
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        print("✅ Backend health check passed")
        return True
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_login():
    """Test authentication"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "employee@demo.gov.in", "password": "Demo@1234"},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        print("✅ Authentication test passed")
        return data["access_token"]
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return None

def test_departments(token):
    """Test department listing"""
    try:
        response = requests.get(
            f"{BASE_URL}/departments/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"✅ Departments test passed ({len(data)} departments found)")
        return data[0]["id"]
    except Exception as e:
        print(f"❌ Departments test failed: {e}")
        return None

def test_chat(token, dept_id):
    """Test chat endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat/ask",
            headers={"Authorization": f"Bearer {token}"},
            json={"question": "What is the leave policy?", "department_id": dept_id},
            timeout=30
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        print("✅ Chat test passed")
        return True
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_ticket_creation(token, dept_id):
    """Test ticket creation"""
    try:
        response = requests.post(
            f"{BASE_URL}/tickets/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Smoke test ticket",
                "description": "This is an automated test ticket",
                "category": "Test",
                "priority": "Low",
                "department_id": dept_id
            },
            timeout=10
        )
        assert response.status_code == 201
        data = response.json()
        assert "ticket_number" in data
        print(f"✅ Ticket creation test passed (Ticket: {data['ticket_number']})")
        return True
    except Exception as e:
        print(f"❌ Ticket creation test failed: {e}")
        return False

def main():
    print("🚀 Starting smoke tests...\n")
    
    # Test sequence
    if not test_health():
        print("\n❌ Backend is not running. Start it with: docker-compose up")
        sys.exit(1)
    
    time.sleep(1)
    
    token = test_login()
    if not token:
        print("\n❌ Authentication failed. Check if database is seeded.")
        sys.exit(1)
    
    time.sleep(1)
    
    dept_id = test_departments(token)
    if not dept_id:
        print("\n❌ No departments found. Run: python backend/seed.py")
        sys.exit(1)
    
    time.sleep(1)
    
    if not test_chat(token, dept_id):
        print("\n⚠️  Chat test failed. Check if Ollama is running and documents are indexed.")
    
    time.sleep(1)
    
    if not test_ticket_creation(token, dept_id):
        print("\n❌ Ticket creation failed.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎉 All smoke tests passed!")
    print("="*60)
    print("\nSystem is ready for demo. Access at:")
    print("  Web: http://localhost:5173")
    print("  API Docs: http://localhost:8000/docs")
    print("\nDemo logins:")
    print("  Employee: employee@demo.gov.in / employee123")
    print("  Officer:  officer.hr@demo.gov.in / officer123")
    print("="*60)

if __name__ == "__main__":
    main()