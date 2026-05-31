"""AGENTIK Orchestrator — Task coordination using Event Bus."""

import asyncio
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from agentik.core.event_bus import Event, EventType, event_bus
from agentik.core.context_builder import Context, context_builder


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Tool:
    """Tool contract as defined in the spec."""
    name: str
    description: str
    validate: Callable = None
    execute: Callable = None
    rollback: Callable = None


@dataclass
class Task:
    """Task data structure."""
    id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    context: Optional[Context] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class Orchestrator:
    """Agent Orchestrator — coordinates tasks and tools using Event Bus.
    
    Ningún módulo puede construir contexto por su cuenta (P4 del spec).
    """
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._tasks: List[Task] = []
        self._event_bus = event_bus
        self._context_builder = context_builder
    
    def register_tool(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return list(self._tools.keys())
    
    async def execute_task(self, task_name: str, user_input: str) -> Dict[str, Any]:
        """Execute a task with full context pipeline."""
        # Create task
        task = Task(id=f"task-{datetime.now().timestamp()}", name=task_name)
        self._tasks.append(task)
        
        try:
            # Publish TaskStarted event
            await self._event_bus.publish(Event(
                event_type=EventType.TASK_STARTED,
                data={"task_id": task.id, "task_name": task_name}
            ))
            
            # Build context (P4: only orchestrator builds context)
            task.context = self._context_builder.build(user_input)
            task.status = TaskStatus.RUNNING
            
            # Execute task
            result = await self._execute_with_tools(task)
            task.result = result
            task.status = TaskStatus.COMPLETED
            
            # Publish TaskCompleted event
            await self._event_bus.publish(Event(
                event_type=EventType.TASK_COMPLETED,
                data={"task_id": task.id, "result": result}
            ))
            
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            
            # Publish TaskFailed event
            await self._event_bus.publish(Event(
                event_type=EventType.TASK_FAILED,
                data={"task_id": task.id, "error": str(e)}
            ))
            
            raise
    
    async def _execute_with_tools(self, task: Task) -> Dict[str, Any]:
        """Execute task using available tools."""
        # Simple execution for now
        return {
            "task_id": task.id,
            "task_name": task.name,
            "status": "completed",
            "context_summary": task.context.final_context if task.context else None
        }
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get task history."""
        return [
            {
                "id": t.id,
                "name": t.name,
                "status": t.status.value,
                "timestamp": t.timestamp.isoformat()
            }
            for t in self._tasks
        ]


# Global orchestrator instance
orchestrator = Orchestrator()
