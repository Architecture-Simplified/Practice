"""
Tests for CRM API
"""
import pytest
from fastapi.testclient import TestClient


class TestCRM:
    """Test CRM endpoints"""

    def test_create_customer(self, client: TestClient, sample_customer_data, sample_user_data):
        """Test creating a new customer"""
        # Register and login to get token
        client.post("/api/auth/register", json=sample_user_data)
        login_response = client.post("/api/auth/login", data={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create customer
        response = client.post("/api/crm/customers", json=sample_customer_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_customer_data["name"]
        assert data["email"] == sample_customer_data["email"]
        assert "id" in data

    def test_get_customers(self, client: TestClient, sample_customer_data, sample_user_data):
        """Test getting all customers"""
        # Setup authentication
        client.post("/api/auth/register", json=sample_user_data)
        login_response = client.post("/api/auth/login", data={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create a customer first
        client.post("/api/crm/customers", json=sample_customer_data, headers=headers)
        
        # Get all customers
        response = client.get("/api/crm/customers", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == sample_customer_data["name"]

    def test_get_customer_by_id(self, client: TestClient, sample_customer_data, sample_user_data):
        """Test getting a specific customer by ID"""
        # Setup authentication
        client.post("/api/auth/register", json=sample_user_data)
        login_response = client.post("/api/auth/login", data={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create a customer
        create_response = client.post("/api/crm/customers", json=sample_customer_data, headers=headers)
        customer_id = create_response.json()["id"]
        
        # Get customer by ID
        response = client.get(f"/api/crm/customers/{customer_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == customer_id
        assert data["name"] == sample_customer_data["name"]

    def test_unauthorized_access(self, client: TestClient, sample_customer_data):
        """Test accessing CRM without authentication"""
        response = client.post("/api/crm/customers", json=sample_customer_data)
        assert response.status_code == 401

        response = client.get("/api/crm/customers")
        assert response.status_code == 401
