"""AGENTIK Security Audit — Integration with security scanning tools."""

import subprocess
import json
import os
from typing import Dict, List, Optional


class SecurityAuditor:
    """Security audit tools integration."""

    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)

    def run_semgrep(self, pattern: str = "auto") -> Dict:
        """Run Semgrep security scanner."""
        try:
            cmd = ["semgrep", "--config", pattern, self.project_root]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {
                "status": "success",
                "output": result.stdout,
                "findings": self._parse_semgrep_output(result.stdout)
            }
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def _parse_semgrep_output(self, output: str) -> List[Dict]:
        """Parse Semgrep output into structured findings."""
        findings = []
        for line in output.split('\n'):
            if line and not line.startswith('#') and '==' not in line:
                findings.append({"line": line})
        return findings

    def run_gitleaks(self) -> Dict:
        """Run Gitleaks secret scanner."""
        try:
            result = subprocess.run(
                ["gitleaks", "detect", "--source", self.project_root, "--report-format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {
                "status": "success",
                "output": result.stdout,
                "clean": result.returncode == 0
            }
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def run_trivy(self, target: str = ".") -> Dict:
        """Run Trivy vulnerability scanner."""
        try:
            result = subprocess.run(
                ["trivy", "fs", "--format", "json", target],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {
                "status": "success",
                "output": result.stdout,
                "vulnerabilities": self._parse_trivy_output(result.stdout)
            }
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def _parse_trivy_output(self, output: str) -> List[Dict]:
        """Parse Trivy output into structured vulnerabilities."""
        try:
            data = json.loads(output)
            return data.get("Results", [])
        except json.JSONDecodeError:
            return []

    def run_nuclei(self, target: str = ".") -> Dict:
        """Run Nuclei vulnerability scanner."""
        try:
            result = subprocess.run(
                ["nuclei", "-target", target, "-json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return {
                "status": "success",
                "output": result.stdout,
                "findings": self._parse_nuclei_output(result.stdout)
            }
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def _parse_nuclei_output(self, output: str) -> List[Dict]:
        """Parse Nuclei output into structured findings."""
        findings = []
        for line in output.split('\n'):
            if line:
                try:
                    findings.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return findings

    def full_audit(self) -> Dict:
        """Run all security audit tools."""
        results = {
            "semgrep": self.run_semgrep(),
            "gitleaks": self.run_gitleaks(),
            "trivy": self.run_trivy(),
            "nuclei": self.run_nuclei()
        }
        return results


# Global security auditor instance
security_auditor = SecurityAuditor()
