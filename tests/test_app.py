import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_and_unregister():
    # Sign up a new participant
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Try duplicate signup
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup_resp.status_code == 400
    assert "already signed up" in dup_resp.json()["detail"]

    # Unregister participant
    del_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert del_resp.status_code == 200
    assert f"Removed {email}" in del_resp.json()["message"]

    # Try to unregister again
    del_resp2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert del_resp2.status_code == 404
    assert "Participant not found" in del_resp2.json()["detail"]
