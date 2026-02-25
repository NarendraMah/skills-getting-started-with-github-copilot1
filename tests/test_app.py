import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    # Arrange
    # ...nothing to arrange for in-memory data...
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

# Test POST /activities/{activity_name}/signup (success)
def test_signup_success():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Confirm participant added
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email in participants

# Test POST /activities/{activity_name}/signup (duplicate)
def test_signup_duplicate():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Test POST /activities/{activity_name}/signup (invalid activity)
def test_signup_invalid_activity():
    # Arrange
    invalid_activity = "nonexistent"
    email = "testuser2@mergington.edu"
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
