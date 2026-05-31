"""AGENTIK Distribution — Package builder."""

import os
import subprocess
from typing import Any, Dict, Optional


class PackageBuilder:
    """Build distribution packages."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
    
    def build_wheel(self) -> Dict[str, Any]:
        """Build wheel package."""
        try:
            result = subprocess.run(
                ["python3", "-m", "build", "--wheel"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
    
    def build_sdist(self) -> Dict[str, Any]:
        """Build source distribution."""
        try:
            result = subprocess.run(
                ["python3", "-m", "build", "--sdist"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
    
    def build_all(self) -> Dict[str, Any]:
        """Build all packages."""
        wheel = self.build_wheel()
        sdist = self.build_sdist()
        
        return {
            "wheel": wheel,
            "sdist": sdist,
            "success": wheel["success"] and sdist["success"]
        }
    
    def upload_to_pypi(self, test: bool = False) -> Dict[str, Any]:
        """Upload to PyPI."""
        try:
            repository = "testpypi" if test else "pypi"
            result = subprocess.run(
                ["python3", "-m", "twine", "upload", "--repository", repository, "dist/*"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "repository": repository
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e),
                "repository": "unknown"
            }


# Global package builder instance
package_builder = PackageBuilder()
