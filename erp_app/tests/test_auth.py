"""
Tests for Authentication API
"""
import pytest
from fastapi.testclient import TestClient


class TestAuth:
    """Test authentication endpoints"""

    def test_register_user(self, client: TestClient, sample_user_data):
        """Test user registration"""
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    def test_register_duplicate_user(self, client: TestClient, sample_user_data):
        """Test registering duplicate user"""
        # Register user first time
        client.post("/api/auth/register", json=sample_user_data)
        # Try to register again
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_login_valid_credentials(self, client: TestClient, sample_user_data):
        """Test login with valid credentials"""
        # Register user first
        client.post("/api/auth/register", json=sample_user_data)
        
        # Login
        login_data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_get_current_user(self, client: TestClient, sample_user_data):
        """Test getting current user info"""
        # Register and login
        client.post("/api/auth/register", json=sample_user_data)
        login_response = client.post("/api/auth/login", data={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
