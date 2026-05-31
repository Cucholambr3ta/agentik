"""Tests for API module."""

import pytest
from fastapi.testclient import TestClient
from agentik.api.server import app


client = TestClient(app)


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"


def test_chat():
    """Test chat endpoint."""
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "timestamp" in data


def test_list_events():
    """Test list events endpoint."""
    response = client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_tasks():
    """Test list tasks endpoint."""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_skills():
    """Test list skills endpoint."""
    response = client.get("/skills")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_run_skill():
    """Test run skill endpoint."""
    response = client.post("/skills/run", json={"skill_name": "test_skill"})
    assert response.status_code == 200
    data = response.json()
    assert data["skill"] == "test_skill"
    assert data["status"] == "executed"
