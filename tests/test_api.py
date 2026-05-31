"""Tests for API module — with real logic verification."""

import pytest
from fastapi.testclient import TestClient
from agentik.api.server import app
from agentik.security.receipts import generate_receipt, verify_receipt
from agentik.core.event_bus import EventBus, Event, EventType


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


# === REAL LOGIC TESTS ===


def test_receipt_hmac_valid_signature():
    """Test that generated receipt has valid HMAC signature."""
    receipt = generate_receipt("test_action", "success")
    
    # Receipt must have required fields
    assert "action" in receipt
    assert "result" in receipt
    assert "signature" in receipt
    assert "timestamp" in receipt
    
    # Signature must be valid
    assert verify_receipt(receipt) is True


def test_receipt_hmac_tampered_detection():
    """Test that tampered receipt is detected."""
    receipt = generate_receipt("test_action", "success")
    
    # Tamper with the receipt
    receipt["result"] = "failure"
    
    # Verification must fail
    assert verify_receipt(receipt) is False


def test_receipt_different_actions_different_signatures():
    """Test that different actions produce different signatures."""
    receipt1 = generate_receipt("action_a", "success")
    receipt2 = generate_receipt("action_b", "success")
    
    assert receipt1["signature"] != receipt2["signature"]


def test_event_bus_delivers_to_subscribers():
    """Test that event bus delivers events to correct subscribers."""
    received_events = []
    
    def handler(event: Event):
        received_events.append(event)
    
    bus = EventBus()
    bus.subscribe(EventType.TASK_STARTED, handler)
    
    # Emit event
    event = Event(event_type=EventType.TASK_STARTED, data={"key": "value"})
    bus.publish_sync(event)
    
    # Handler should have received the event
    assert len(received_events) == 1
    assert received_events[0].event_type == EventType.TASK_STARTED
    assert received_events[0].data == {"key": "value"}


def test_event_bus_does_not_deliver_to_wrong_subscribers():
    """Test that event bus does not deliver to wrong subscribers."""
    received_events = []
    
    def handler(event: Event):
        received_events.append(event)
    
    bus = EventBus()
    bus.subscribe(EventType.TASK_FAILED, handler)
    
    # Emit different event
    event = Event(event_type=EventType.TASK_STARTED, data={})
    bus.publish_sync(event)
    
    # Handler should not have received anything
    assert len(received_events) == 0


def test_event_bus_multiple_subscribers():
    """Test that event bus delivers to multiple subscribers."""
    received_a = []
    received_b = []
    
    def handler_a(event: Event):
        received_a.append(event)
    
    def handler_b(event: Event):
        received_b.append(event)
    
    bus = EventBus()
    bus.subscribe(EventType.TASK_STARTED, handler_a)
    bus.subscribe(EventType.TASK_STARTED, handler_b)
    
    event = Event(event_type=EventType.TASK_STARTED, data={})
    bus.publish_sync(event)
    
    assert len(received_a) == 1
    assert len(received_b) == 1

