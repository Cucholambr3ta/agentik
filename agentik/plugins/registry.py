"""AGENTIK Plugins — Plugin registry."""

import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from agentik.plugins.contract import PluginContract


class PluginRegistry:
    """Registry for managing plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, PluginContract] = {}
        self._plugin_info: Dict[str, Dict[str, Any]] = {}
    
    def register_plugin(self, plugin: PluginContract) -> bool:
        """Register a plugin."""
        try:
            # Register the plugin
            tools = plugin.register()
            
            self._plugins[plugin.name] = plugin
            self._plugin_info[plugin.name] = {
                **plugin.get_info(),
                "registered_at": datetime.now().isoformat(),
                "tools": tools
            }
            
            return True
        except Exception as e:
            return False
    
    def unregister_plugin(self, name: str) -> bool:
        """Unregister a plugin."""
        if name in self._plugins:
            try:
                self._plugins[name].unregister()
                del self._plugins[name]
                del self._plugin_info[name]
                return True
            except Exception:
                return False
        return False
    
    def get_plugin(self, name: str) -> Optional[PluginContract]:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all registered plugins."""
        return list(self._plugin_info.values())
    
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get all tools from all plugins."""
        tools = []
        for plugin_name, plugin in self._plugins.items():
            plugin_tools = plugin.get_tools()
            for tool in plugin_tools:
                tool["plugin"] = plugin_name
                tools.append(tool)
        return tools


# Global plugin registry instance
plugin_registry = PluginRegistry()
