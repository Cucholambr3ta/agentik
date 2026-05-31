"""AGENTIK History — Persistent command history storage."""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class CommandHistory:
    """Persistent command history storage."""
    
    def __init__(self, history_file: str = "~/.agentik/history.json"):
        self.history_file = os.path.expanduser(history_file)
        self._ensure_directory()
        self.history = self._load()
    
    def _ensure_directory(self):
        """Ensure the directory exists."""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
    
    def _load(self) -> List[Dict]:
        """Load history from file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save(self):
        """Save history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add(self, command: str, output: str, exit_code: int = 0) -> Dict:
        """Add a command to history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "output": output[:1000],  # Truncate long outputs
            "exit_code": exit_code
        }
        self.history.append(entry)
        self._save()
        return entry
    
    def get_recent(self, count: int = 10) -> List[Dict]:
        """Get recent command history."""
        return self.history[-count:]
    
    def search(self, query: str) -> List[Dict]:
        """Search command history."""
        return [h for h in self.history if query.lower() in h["command"].lower()]
    
    def clear(self):
        """Clear command history."""
        self.history = []
        self._save()
    
    def count(self) -> int:
        """Get total number of commands in history."""
        return len(self.history)


# Global history instance
history = CommandHistory()
