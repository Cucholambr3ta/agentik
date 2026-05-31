"""Tests for Event Bus module."""

import pytest
from agentik.core.event_bus import EventBus, Event, EventType


def test_event_bus_subscribe():
    """Test subscribing to an event."""
    bus = EventBus()
    received = []
    
    def handler(event):
        received.append(event)
    
    bus.subscribe(EventType.TASK_STARTED, handler)
    assert EventType.TASK_STARTED in bus._subscribers


def test_event_bus_publish():
    """Test publishing an event."""
    bus = EventBus()
    received = []
    
    def handler(event):
        received.append(event)
    
    bus.subscribe(EventType.TASK_STARTED, handler)
    
    event = Event(event_type=EventType.TASK_STARTED, data={"task_id": "123"})
    bus.publish_sync(event)
    
    assert len(received) == 1
    assert received[0].event_type == EventType.TASK_STARTED


def test_event_bus_history():
    """Test event history."""
    bus = EventBus()
    
    event1 = Event(event_type=EventType.TASK_STARTED, data={})
    event2 = Event(event_type=EventType.TASK_COMPLETED, data={})
    
    bus.publish_sync(event1)
    bus.publish_sync(event2)
    
    history = bus.get_history()
    assert len(history) == 2


def test_event_bus_history_filter():
    """Test filtering event history."""
    bus = EventBus()
    
    event1 = Event(event_type=EventType.TASK_STARTED, data={})
    event2 = Event(event_type=EventType.TASK_COMPLETED, data={})
    
    bus.publish_sync(event1)
    bus.publish_sync(event2)
    
    history = bus.get_history(EventType.TASK_STARTED)
    assert len(history) == 1
    assert history[0].event_type == EventType.TASK_STARTED
