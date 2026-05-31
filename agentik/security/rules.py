"""AGENTIK Aegis — Security rules for vulnerability detection."""

import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Vulnerability severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityRule:
    """Security rule data structure."""
    name: str
    description: str
    pattern: str
    severity: Severity
    cwe: Optional[str] = None


# Default security rules
DEFAULT_RULES = [
    SecurityRule(
        name="sql_injection",
        description="SQL Injection vulnerability",
        pattern=r"(execute|cursor\.execute)\s*\(\s*['\"].*%s.*['\"]",
        severity=Severity.HIGH,
        cwe="CWE-89"
    ),
    SecurityRule(
        name="xss_vulnerability",
        description="Cross-Site Scripting vulnerability",
        pattern=r"innerHTML\s*=\s*.*\+|document\.write\s*\(",
        severity=Severity.MEDIUM,
        cwe="CWE-79"
    ),
    SecurityRule(
        name="command_injection",
        description="Command Injection vulnerability",
        pattern=r"os\.system\s*\(|subprocess\.call\s*\(\s*['\"].*\+",
        severity=Severity.HIGH,
        cwe="CWE-78"
    ),
    SecurityRule(
        name="hardcoded_secret",
        description="Hardcoded secret or password",
        pattern=r"(password|secret|api_key|token)\s*=\s*['\"][^'\"]+['\"]",
        severity=Severity.CRITICAL,
        cwe="CWE-798"
    ),
    SecurityRule(
        name="eval_usage",
        description="Use of eval() function",
        pattern=r"eval\s*\(",
        severity=Severity.HIGH,
        cwe="CWE-95"
    ),
    SecurityRule(
        name="pickle_usage",
        description="Use of pickle for deserialization",
        pattern=r"pickle\.loads?\s*\(",
        severity=Severity.MEDIUM,
        cwe="CWE-502"
    ),
]


class SecurityRuleEngine:
    """Security rule engine for vulnerability detection."""
    
    def __init__(self, rules: List[SecurityRule] = None):
        self.rules = rules or DEFAULT_RULES
    
    def scan_code(self, code: str) -> List[Dict[str, Any]]:
        """Scan code for vulnerabilities."""
        findings = []
        
        for rule in self.rules:
            matches = re.finditer(rule.pattern, code, re.IGNORECASE)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                findings.append({
                    "rule": rule.name,
                    "description": rule.description,
                    "severity": rule.severity.value,
                    "cwe": rule.cwe,
                    "line": line_number,
                    "match": match.group()
                })
        
        return findings
    
    def scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan a file for vulnerabilities."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return self.scan_code(code)
        except Exception:
            return []


# Global security rule engine instance
security_rules = SecurityRuleEngine()
