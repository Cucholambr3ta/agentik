"""Tests for Plugins module."""

import pytest
from agentik.plugins.contract import PluginContract
from agentik.plugins.registry import PluginRegistry, plugin_registry
from agentik.plugins.discovery import PluginDiscovery


class TestPlugin(PluginContract):
    """Test plugin implementation."""
    
    @property
    def name(self) -> str:
        return "test_plugin"
    
    @property
    def description(self) -> str:
        return "A test plugin"
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    def register(self) -> dict:
        return {"test_tool": "description"}
    
    def unregister(self) -> bool:
        return True
    
    def get_tools(self) -> list:
        return [{"name": "test_tool", "description": "Test tool"}]


def test_plugin_contract():
    """Test plugin contract."""
    plugin = TestPlugin()
    assert plugin.name == "test_plugin"
    assert plugin.description == "A test plugin"
    assert plugin.version == "0.1.0"


def test_plugin_registry_register():
    """Test registering a plugin."""
    registry = PluginRegistry()
    plugin = TestPlugin()
    
    result = registry.register_plugin(plugin)
    assert result is True
    assert "test_plugin" in [p["name"] for p in registry.list_plugins()]


def test_plugin_registry_unregister():
    """Test unregistering a plugin."""
    registry = PluginRegistry()
    plugin = TestPlugin()
    
    registry.register_plugin(plugin)
    result = registry.unregister_plugin("test_plugin")
    assert result is True
    assert len(registry.list_plugins()) == 0


def test_plugin_registry_get_tools():
    """Test getting all tools."""
    registry = PluginRegistry()
    plugin = TestPlugin()
    
    registry.register_plugin(plugin)
    tools = registry.get_all_tools()
    
    assert len(tools) == 1
    assert tools[0]["name"] == "test_tool"


def test_plugin_discovery():
    """Test plugin discovery."""
    discovery = PluginDiscovery(plugin_dirs=[])
    discovered = discovery.discover_plugins()
    assert isinstance(discovered, list)
