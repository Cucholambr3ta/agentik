"""AGENTIK GitNexus — Code analysis integration with GitNexus."""

import subprocess
import json
import os
from typing import Dict, List, Optional


class GitNexusAnalyzer:
    """GitNexus code analysis integration."""

    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)

    def analyze(self) -> Dict:
        """Run GitNexus analysis on the project."""
        try:
            result = subprocess.run(
                ["gitnexus", "analyze"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def query(self, query: str) -> Dict:
        """Query GitNexus for code patterns."""
        try:
            result = subprocess.run(
                ["gitnexus", "query", query],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def impact(self, symbol: str, direction: str = "upstream") -> Dict:
        """Analyze impact of changing a symbol."""
        try:
            result = subprocess.run(
                ["gitnexus", "impact", symbol, "--direction", direction],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def context(self, name: str) -> Dict:
        """Get full context for a symbol."""
        try:
            result = subprocess.run(
                ["gitnexus", "context", name],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def status(self) -> Dict:
        """Get GitNexus status."""
        try:
            result = subprocess.run(
                ["gitnexus", "status"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def clusters(self) -> Dict:
        """List all functional clusters."""
        try:
            result = subprocess.run(
                ["gitnexus", "clusters"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def processes(self) -> Dict:
        """List all execution flows."""
        try:
            result = subprocess.run(
                ["gitnexus", "processes"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {"status": "success", "output": result.stdout}
        except Exception as e:
            return {"status": "failure", "error": str(e)}


# Global GitNexus analyzer instance
gitnexus = GitNexusAnalyzer()
