import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_generate_social_content_unauthorized():
    """Test content generation without authentication"""
    response = client.post(
        "/api/v1/content/generate/social",
        json={
            "topic": "Test topic",
            "platforms": ["instagram"],
            "tone": "professional"
        }
    )
    # Should require authentication
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_analytics_overview_unauthorized():
    """Test analytics without authentication"""
    response = client.get("/api/v1/analytics/overview?user_id=1")
    assert response.status_code == 401


def test_payment_create_checkout_unauthorized():
    """Test payment checkout without authentication"""
    response = client.post(
        "/api/v1/payments/create-checkout-session",
        json={
            "tier": "starter",
            "success_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/cancel"
        }
    )
    assert response.status_code == 401


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers


def test_api_docs_accessible():
    """Test API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test OpenAPI schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
