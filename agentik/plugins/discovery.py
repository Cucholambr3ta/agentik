"""AGENTIK Plugins — Plugin discovery."""

import importlib
import os
import sys
from typing import Any, Dict, List, Optional

from agentik.plugins.contract import PluginContract
from agentik.plugins.registry import plugin_registry


class PluginDiscovery:
    """Discover and load plugins automatically."""
    
    def __init__(self, plugin_dirs: List[str] = None):
        self.plugin_dirs = plugin_dirs or [
            os.path.expanduser("~/.agentik/plugins"),
            os.path.join(os.path.dirname(__file__), "builtin")
        ]
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins."""
        discovered = []
        
        for plugin_dir in self.plugin_dirs:
            if os.path.exists(plugin_dir):
                for item in os.listdir(plugin_dir):
                    if item.endswith("_plugin.py"):
                        plugin_name = item[:-3]  # Remove .py
                        discovered.append(plugin_name)
        
        return discovered
    
    def load_plugin(self, plugin_name: str) -> Optional[PluginContract]:
        """Load a plugin by name."""
        try:
            # Try to import the plugin module
            module_name = f"agentik.plugins.builtin.{plugin_name}"
            if module_name not in sys.modules:
                module = importlib.import_module(module_name)
            else:
                module = sys.modules[module_name]
            
            # Look for plugin class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, PluginContract) and 
                    attr != PluginContract):
                    return attr()
            
            return None
        except Exception:
            return None
    
    def load_all_plugins(self) -> int:
        """Load all discovered plugins."""
        discovered = self.discover_plugins()
        loaded = 0
        
        for plugin_name in discovered:
            plugin = self.load_plugin(plugin_name)
            if plugin:
                if plugin_registry.register_plugin(plugin):
                    loaded += 1
        
        return loaded


# Global plugin discovery instance
plugin_discovery = PluginDiscovery()
