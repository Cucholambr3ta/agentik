"""AGENTIK Self-improvement — Patcher for generating patches."""

import os
import difflib
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Patch:
    """Patch data structure."""
    id: str
    file_path: str
    original_content: str
    new_content: str
    description: str
    created: datetime = field(default_factory=datetime.now)
    applied: bool = False


class Patcher:
    """Generate and apply patches."""
    
    def __init__(self):
        self._patches: List[Patch] = []
    
    def create_patch(self, file_path: str, original: str, new: str, description: str) -> Patch:
        """Create a patch."""
        patch = Patch(
            id=f"patch-{datetime.now().timestamp()}",
            file_path=file_path,
            original_content=original,
            new_content=new,
            description=description
        )
        
        self._patches.append(patch)
        return patch
    
    def generate_diff(self, patch: Patch) -> str:
        """Generate diff for a patch."""
        diff = difflib.unified_diff(
            patch.original_content.splitlines(keepends=True),
            patch.new_content.splitlines(keepends=True),
            fromfile=f"a/{patch.file_path}",
            tofile=f"b/{patch.file_path}"
        )
        return ''.join(diff)
    
    def apply_patch(self, patch: Patch) -> bool:
        """Apply a patch."""
        try:
            with open(patch.file_path, 'w') as f:
                f.write(patch.new_content)
            patch.applied = True
            return True
        except Exception:
            return False
    
    def get_patches(self) -> List[Patch]:
        """Get all patches."""
        return self._patches.copy()
    
    def get_pending_patches(self) -> List[Patch]:
        """Get patches that haven't been applied."""
        return [p for p in self._patches if not p.applied]


# Global patcher instance
patcher = Patcher()
