import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def user_credentials():
    """Fixture that returns unique user credentials without registering"""
    timestamp = int(time.time() * 1000)
    return {
        "username": f"testuser{timestamp}",
        "password": "magikarpUsedSplash123"
    }


@pytest.fixture
def registered_user(user_credentials):
    """Fixture that registers a unique user and returns credentials"""
    requests.post(f"{BASE_URL}/auth/register", json=user_credentials)
    return user_credentials


@pytest.fixture
def auth_token(registered_user):
    """Fixture that logs in a registered user and returns the JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", json=registered_user)
    return response.json()["access_token"]
