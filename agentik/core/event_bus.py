"""AGENTIK Event Bus — Asynchronous publish/subscribe system."""

import asyncio
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventType(Enum):
    """Event types as defined in the spec."""
    USER_MESSAGE_RECEIVED = "UserMessageReceived"
    TASK_STARTED = "TaskStarted"
    TASK_COMPLETED = "TaskCompleted"
    TASK_FAILED = "TaskFailed"
    CODE_MODIFIED = "CodeModified"
    PIPELINE_STARTED = "PipelineStarted"
    PIPELINE_PASSED = "PipelinePassed"
    PIPELINE_FAILED = "PipelineFailed"
    LESSON_CREATED = "LessonCreated"
    LESSON_UPDATED = "LessonUpdated"
    SKILL_CREATED = "SkillCreated"
    SKILL_EXECUTED = "SkillExecuted"
    SECURITY_ISSUE_DETECTED = "SecurityIssueDetected"
    RECEIPT_GENERATED = "ReceiptGenerated"


@dataclass
class Event:
    """Event data structure."""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "system"


class EventBus:
    """Asynchronous publish/subscribe event bus."""
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._history: List[Event] = []
    
    def subscribe(self, event_type: EventType, callback: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
    
    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers."""
        self._history.append(event)
        
        if event.event_type in self._subscribers:
            for callback in self._subscribers[event.event_type]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
    
    def publish_sync(self, event: Event) -> None:
        """Publish an event synchronously."""
        self._history.append(event)
        
        if event.event_type in self._subscribers:
            for callback in self._subscribers[event.event_type]:
                callback(event)
    
    def get_history(self, event_type: Optional[EventType] = None) -> List[Event]:
        """Get event history, optionally filtered by type."""
        if event_type:
            return [e for e in self._history if e.event_type == event_type]
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear event history."""
        self._history.clear()


# Global event bus instance
event_bus = EventBus()
