"""AGENTIK Aegis — SAST/DAST security scanner."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from agentik.security.rules import security_rules, Severity


@dataclass
class ScanResult:
    """Security scan result."""
    timestamp: datetime
    file_path: Optional[str]
    findings: List[Dict[str, Any]]
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


class AegisScanner:
    """SAST/DAST security scanner."""
    
    def __init__(self):
        self._scan_history: List[ScanResult] = []
    
    def scan_code(self, code: str, file_path: str = None) -> ScanResult:
        """Scan code for vulnerabilities."""
        findings = security_rules.scan_code(code)
        
        result = ScanResult(
            timestamp=datetime.now(),
            file_path=file_path,
            findings=findings,
            total_findings=len(findings),
            critical_count=sum(1 for f in findings if f["severity"] == "critical"),
            high_count=sum(1 for f in findings if f["severity"] == "high"),
            medium_count=sum(1 for f in findings if f["severity"] == "medium"),
            low_count=sum(1 for f in findings if f["severity"] == "low")
        )
        
        self._scan_history.append(result)
        return result
    
    def scan_file(self, file_path: str) -> ScanResult:
        """Scan a file for vulnerabilities."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return self.scan_code(code, file_path)
        except Exception as e:
            return ScanResult(
                timestamp=datetime.now(),
                file_path=file_path,
                findings=[],
                total_findings=0,
                critical_count=0,
                high_count=0,
                medium_count=0,
                low_count=0
            )
    
    def scan_directory(self, directory: str) -> List[ScanResult]:
        """Scan a directory for vulnerabilities."""
        import os
        results = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results.append(self.scan_file(file_path))
        
        return results
    
    def get_scan_history(self) -> List[Dict[str, Any]]:
        """Get scan history."""
        return [
            {
                "timestamp": r.timestamp.isoformat(),
                "file_path": r.file_path,
                "total_findings": r.total_findings,
                "critical_count": r.critical_count,
                "high_count": r.high_count
            }
            for r in self._scan_history
        ]
    
    def has_critical_findings(self) -> bool:
        """Check if there are any critical findings."""
        return any(r.critical_count > 0 for r in self._scan_history)


# Global Aegis scanner instance
aegis = AegisScanner()
