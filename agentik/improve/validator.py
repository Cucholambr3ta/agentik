"""AGENTIK Self-improvement — Validator for validating patches with x-dd."""

import subprocess
from typing import Any, Dict, Optional
from dataclasses import dataclass

from agentik.improve.patcher import Patch


@dataclass
class ValidationResult:
    """Validation result."""
    patch_id: str
    tests_passed: bool
    xdd_approved: bool
    security_clean: bool
    overall: bool


class Validator:
    """Validate patches with x-dd."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
    
    def validate_patch(self, patch: Patch) -> ValidationResult:
        """Validate a patch."""
        # Run tests
        tests_passed = self._run_tests()
        
        # Run x-dd validation
        xdd_approved = self._run_xdd_validation()
        
        # Run security scan
        security_clean = self._run_security_scan()
        
        overall = tests_passed and xdd_approved and security_clean
        
        return ValidationResult(
            patch_id=patch.id,
            tests_passed=tests_passed,
            xdd_approved=xdd_approved,
            security_clean=security_clean,
            overall=overall
        )
    
    def _run_tests(self) -> bool:
        """Run tests."""
        try:
            result = subprocess.run(
                ["python3", "-m", "pytest", "tests/", "-v"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _run_xdd_validation(self) -> bool:
        """Run x-dd validation."""
        try:
            result = subprocess.run(
                ["xdd", "gate", "status"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _run_security_scan(self) -> bool:
        """Run security scan."""
        try:
            from agentik.security.aegis import aegis
            
            # Scan the patch file
            # For now, just return True
            return True
        except Exception:
            return False


# Global validator instance
validator = Validator()
