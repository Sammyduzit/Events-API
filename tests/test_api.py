import requests


def test_health_check(base_url):
    """Tests the health endpoint functionality"""
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_event_creation(auth_token, base_url):
    """Tests creation of an event"""
    #Arrange
    event_data = {
    "title": "Magikarp Splash Tournament",
    "description": "The ultimate show off event for Magikarps legendary attack: Splash",
    "date": "2026-04-01T18:00:00",
    "location": "P-Diddys Pool",
    "capacity": 42,
    "is_public": True,
    "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    #Act
    response = requests.post(f"{base_url}/events",
                             json=event_data,
                             headers=headers)

    #Assert
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Magikarp Splash Tournament"
    assert data["description"] == "The ultimate show off event for Magikarps legendary attack: Splash"
    assert data["date"] == "2026-04-01T18:00:00"
    assert data["location"] == "P-Diddys Pool"
    assert data["capacity"] == 42


def test_user_registration(user_credentials, base_url):
    """Tests that a new user can register successfully"""
    #Act
    response = requests.post(f"{base_url}/auth/register", json=user_credentials)

    #Assert
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == user_credentials["username"]
    assert "password" not in data["user"]


def test_login_returns_jwt_token(registered_user, base_url):
    """Tests that login with valid credentials returns a JWT access token"""
    #Act
    response = requests.post(f"{base_url}/auth/login", json=registered_user)

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert len(data["access_token"]) > 0


def test_event_creation_without_token(base_url):
    """Tests that creating an event without authentication returns 401"""
    #Arrange
    event_data = {
        "title": "Unauthorized Magikarp",
        "date": "2026-04-01T10:00:00"
    }

    #Act
    response = requests.post(f"{base_url}/events", json=event_data)

    #Assert
    assert response.status_code == 401


def test_duplicate_registration_returns_400(registered_user, base_url):
    """Tests that registering with an already taken username returns 400"""
    #Act: register again with the same credentials
    response = requests.post(f"{base_url}/auth/register", json=registered_user)

    #Assert
    assert response.status_code == 400


def test_login_with_wrong_password_returns_401(registered_user, base_url):
    """Tests that login with an incorrect password returns 401"""
    #Arrange
    wrong_credentials = {
        "username": registered_user["username"],
        "password": "MagikarpImposter"
    }

    #Act
    response = requests.post(f"{base_url}/auth/login", json=wrong_credentials)

    #Assert
    assert response.status_code == 401


def test_rsvp_to_private_event_without_auth_returns_401(auth_token, base_url):
    """Tests that RSVP to a private event without authentication returns 401"""
    #Arrange: create a private event
    event_data = {
        "title": "Private Magikarp VIP Event",
        "date": "2026-04-01T20:00:00",
        "is_public": False,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = requests.post(f"{base_url}/events", json=event_data, headers=headers)
    assert create_response.status_code == 201
    event_id = create_response.json()["id"]

    #Act: RSVP without authentication
    rsvp_response = requests.post(f"{base_url}/rsvps/event/{event_id}", json={})

    #Assert
    assert rsvp_response.status_code == 401


def test_rsvp_to_public_event(auth_token, base_url):
    """Tests that a user can RSVP to a public event without authentication"""
    #Arrange: create a public event
    event_data = {
        "title": "Open Public Magikarp Meetup",
        "date": "2026-04-01T12:00:00",
        "is_public": True,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = requests.post(f"{base_url}/events", json=event_data, headers=headers)
    assert create_response.status_code == 201
    event_id = create_response.json()["id"]

    #Act: RSVP without authentication
    rsvp_response = requests.post(f"{base_url}/rsvps/event/{event_id}", json={})

    #Assert
    assert rsvp_response.status_code == 201
    data = rsvp_response.json()
    assert data["event_id"] == event_id
    assert data["attending"] is True
