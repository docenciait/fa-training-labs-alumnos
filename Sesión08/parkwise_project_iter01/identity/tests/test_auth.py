from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app


client = TestClient(app)

def test_register_and_login():
    response = client.post("/auth/register", json={
        "username": "alice", "password": "1234", "role": "admin"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    login_response = client.post("/auth/login", json={
        "username": "alice", "password": "1234"
    })
    assert login_response.status_code == 200
    assert login_response.json()["access_token"]
