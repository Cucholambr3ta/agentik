"""AGENTIK Plugins — Plugin contract."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class PluginContract(ABC):
    """Plugin contract that all plugins must implement."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @abstractmethod
    def register(self) -> Dict[str, Any]:
        """Register the plugin and return tools/capabilities."""
        pass
    
    @abstractmethod
    def unregister(self) -> bool:
        """Unregister the plugin."""
        pass
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get tools provided by this plugin."""
        return []
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "tools": self.get_tools()
        }
