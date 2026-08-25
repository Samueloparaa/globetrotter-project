"""
Basic pytest tests for Phase 1 of the GlobeTrotter Travel Assistant.

Covers the minimum required by the assignment:
- /register returns 200
- /login returns a token
- /destinations returns a list

Adjust the import below (`from main import app`) if your FastAPI
app instance lives in a different file/module.
"""

import pytest
from fastapi.testclient import TestClient

from main import app  # change "main" if your app file is named differently

client = TestClient(app)

# Use a distinctive test email so repeated test runs don't collide
# with existing accounts in your dev database.
TEST_USER = {
    "email": "phase1_test_user@example.com",
    "password": "TestPassword123!"
}


def test_register_returns_200():
    response = client.post("/register", json=TEST_USER)
    # Accept 200 or 201 depending on your implementation's convention,
    # and 400 if the user already exists from a previous test run.
    assert response.status_code in (200, 201, 400)


def test_login_returns_token():
    # Make sure the user exists first
    client.post("/register", json=TEST_USER)

    response = client.post("/login", json=TEST_USER)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_destinations_returns_list():
    response = client.get("/destinations")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.fixture
def auth_headers():
    """Registers/logs in a user and returns Authorization headers for
    testing protected endpoints."""
    client.post("/register", json=TEST_USER)
    login_response = client.post("/login", json=TEST_USER)
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_recommendations_requires_auth_and_returns_200(auth_headers):
    response = client.get("/recommendations", headers=auth_headers)
    assert response.status_code == 200


def test_create_and_list_itineraries(auth_headers):
    new_itinerary = {
        "title": "Test Trip to Tokyo",
        "destination_id": 3
    }
    create_response = client.post(
        "/itineraries", json=new_itinerary, headers=auth_headers
    )
    assert create_response.status_code in (200, 201)

    list_response = client.get("/itineraries", headers=auth_headers)
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
