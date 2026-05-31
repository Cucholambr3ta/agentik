"""Tests for Orchestrator module."""

import pytest
import asyncio
from agentik.core.orchestrator import Orchestrator, Tool, Task, TaskStatus


def test_orchestrator_register_tool():
    """Test registering a tool."""
    orch = Orchestrator()
    
    tool = Tool(
        name="test_tool",
        description="A test tool"
    )
    
    orch.register_tool(tool)
    assert "test_tool" in orch.list_tools()


def test_orchestrator_get_tool():
    """Test getting a tool."""
    orch = Orchestrator()
    
    tool = Tool(
        name="test_tool",
        description="A test tool"
    )
    
    orch.register_tool(tool)
    retrieved = orch.get_tool("test_tool")
    
    assert retrieved is not None
    assert retrieved.name == "test_tool"


def test_orchestrator_list_tools():
    """Test listing tools."""
    orch = Orchestrator()
    
    tool1 = Tool(name="tool1", description="Tool 1")
    tool2 = Tool(name="tool2", description="Tool 2")
    
    orch.register_tool(tool1)
    orch.register_tool(tool2)
    
    tools = orch.list_tools()
    assert len(tools) == 2
    assert "tool1" in tools
    assert "tool2" in tools


def test_orchestrator_task_history():
    """Test task history."""
    orch = Orchestrator()
    history = orch.get_task_history()
    
    assert isinstance(history, list)
    assert len(history) == 0
