"""AGENTIK Distribution — Auto-update checker."""

import json
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, Optional
from urllib.request import urlopen
from urllib.error import URLError


class UpdateChecker:
    """Check for updates from PyPI or GitHub."""
    
    def __init__(self, current_version: str = "0.1.0"):
        self.current_version = current_version
        self._last_check: Optional[datetime] = None
    
    def check_pypi(self) -> Dict[str, Any]:
        """Check for updates on PyPI."""
        try:
            url = "https://pypi.org/pypi/agentik/json"
            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                latest_version = data["info"]["version"]
                
                return {
                    "current": self.current_version,
                    "latest": latest_version,
                    "update_available": self._version_compare(latest_version, self.current_version),
                    "source": "pypi"
                }
        except (URLError, Exception) as e:
            return {
                "current": self.current_version,
                "latest": None,
                "update_available": False,
                "source": "pypi",
                "error": str(e)
            }
    
    def check_github(self, repo: str = "Cucholambr3ta/agentik") -> Dict[str, Any]:
        """Check for updates on GitHub."""
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                latest_version = data["tag_name"].lstrip("v")
                
                return {
                    "current": self.current_version,
                    "latest": latest_version,
                    "update_available": self._version_compare(latest_version, self.current_version),
                    "source": "github",
                    "release_url": data.get("html_url")
                }
        except (URLError, Exception) as e:
            return {
                "current": self.current_version,
                "latest": None,
                "update_available": False,
                "source": "github",
                "error": str(e)
            }
    
    def _version_compare(self, latest: str, current: str) -> bool:
        """Compare versions and return True if update available."""
        try:
            latest_parts = [int(x) for x in latest.split(".")]
            current_parts = [int(x) for x in current.split(".")]
            
            for i in range(max(len(latest_parts), len(current_parts))):
                l = latest_parts[i] if i < len(latest_parts) else 0
                c = current_parts[i] if i < len(current_parts) else 0
                
                if l > c:
                    return True
                elif l < c:
                    return False
            
            return False
        except (ValueError, AttributeError):
            return False
    
    def get_current_version(self) -> str:
        """Get current version from VERSION file."""
        try:
            version_file = os.path.join(os.path.dirname(__file__), "..", "..", "VERSION")
            with open(version_file, 'r') as f:
                return f.read().strip()
        except Exception:
            return self.current_version


# Global update checker instance
update_checker = UpdateChecker()
