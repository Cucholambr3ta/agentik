"""AGENTIK Aegis — Security rules for vulnerability detection."""

import ast
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
    use_ast: bool = False


# Default security rules
DEFAULT_RULES = [
    SecurityRule(
        name="sql_injection",
        description="SQL Injection vulnerability",
        pattern=r"(execute|cursor\.execute)\s*\(\s*['\"].*%s.*['\"]",
        severity=Severity.HIGH,
        cwe="CWE-89",
        use_ast=True
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
        cwe="CWE-78",
        use_ast=True
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
        cwe="CWE-95",
        use_ast=True
    ),
    SecurityRule(
        name="pickle_usage",
        description="Use of pickle for deserialization",
        pattern=r"pickle\.loads?\s*\(",
        severity=Severity.MEDIUM,
        cwe="CWE-502"
    ),
]


class SQLInjectionDetector(ast.NodeVisitor):
    """AST-based SQL injection detector."""
    
    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
    
    def visit_Call(self, node: ast.Call) -> None:
        """Detect SQL injection in function calls."""
        # Check for execute("...%s...") patterns
        if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
            if node.args:
                arg = node.args[0]
                # Check for string formatting with %
                if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
                    self.findings.append({
                        "rule": "sql_injection",
                        "description": "SQL Injection: string formatting in execute()",
                        "severity": "high",
                        "cwe": "CWE-89",
                        "line": node.lineno,
                        "match": f"execute(... % ...)"
                    })
                # Check for f-string or format call
                elif isinstance(arg, ast.JoinedStr):
                    self.findings.append({
                        "rule": "sql_injection",
                        "description": "SQL Injection: f-string in execute()",
                        "severity": "high",
                        "cwe": "CWE-89",
                        "line": node.lineno,
                        "match": f"execute(f'...')"
                    })
                # Check for string concatenation
                elif isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                    self.findings.append({
                        "rule": "sql_injection",
                        "description": "SQL Injection: string concatenation in execute()",
                        "severity": "high",
                        "cwe": "CWE-89",
                        "line": node.lineno,
                        "match": "execute(... + ...)"
                    })
        
        # Check for cursor.execute patterns
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == "cursor" and node.func.attr == "execute":
                if node.args and isinstance(node.args[0], ast.BinOp):
                    self.findings.append({
                        "rule": "sql_injection",
                        "description": "SQL Injection: dynamic query in cursor.execute()",
                        "severity": "high",
                        "cwe": "CWE-89",
                        "line": node.lineno,
                        "match": "cursor.execute(...)"
                    })
        
        self.generic_visit(node)


class CommandInjectionDetector(ast.NodeVisitor):
    """AST-based command injection detector."""
    
    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
    
    def visit_Call(self, node: ast.Call) -> None:
        """Detect command injection in function calls."""
        # Check for os.system(...)
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == "os" and node.func.attr == "system":
                if node.args:
                    # Check for string concatenation
                    if isinstance(node.args[0], ast.BinOp) and isinstance(node.args[0].op, ast.Add):
                        self.findings.append({
                            "rule": "command_injection",
                            "description": "Command Injection: string concatenation in os.system()",
                            "severity": "high",
                            "cwe": "CWE-78",
                            "line": node.lineno,
                            "match": "os.system(... + ...)"
                        })
                    # Check for direct string (potential command injection)
                    elif isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        self.findings.append({
                            "rule": "command_injection",
                            "description": "Command Injection: direct command in os.system()",
                            "severity": "high",
                            "cwe": "CWE-78",
                            "line": node.lineno,
                            "match": f"os.system(\"{node.args[0].value}\")"
                        })
        
        # Check for subprocess.call(...)
        elif isinstance(node.func, ast.Name) and node.func.id == "subprocess":
            if node.args and isinstance(node.args[0], ast.BinOp) and isinstance(node.args[0].op, ast.Add):
                self.findings.append({
                    "rule": "command_injection",
                    "description": "Command Injection: string concatenation in subprocess.call()",
                    "severity": "high",
                    "cwe": "CWE-78",
                    "line": node.lineno,
                    "match": "subprocess.call(... + ...)"
                })
        
        self.generic_visit(node)


class EvalDetector(ast.NodeVisitor):
    """AST-based eval() usage detector."""
    
    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
    
    def visit_Call(self, node: ast.Call) -> None:
        """Detect eval() usage."""
        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            self.findings.append({
                "rule": "eval_usage",
                "description": "Use of eval() function",
                "severity": "high",
                "cwe": "CWE-95",
                "line": node.lineno,
                "match": "eval(...)"
            })
        
        self.generic_visit(node)


class SecurityRuleEngine:
    """Security rule engine for vulnerability detection."""
    
    def __init__(self, rules: List[SecurityRule] = None):
        self.rules = rules or DEFAULT_RULES
    
    def scan_code(self, code: str) -> List[Dict[str, Any]]:
        """Scan code for vulnerabilities using both AST and regex."""
        findings = []
        
        # AST-based detection for rules that support it
        try:
            tree = ast.parse(code)
            
            # Run AST detectors
            ast_detectors = [
                SQLInjectionDetector(),
                CommandInjectionDetector(),
                EvalDetector()
            ]
            
            for detector in ast_detectors:
                detector.visit(tree)
                findings.extend(detector.findings)
        except SyntaxError:
            # If AST parsing fails, fall back to regex only
            pass
        
        # Regex-based detection for rules without AST support
        for rule in self.rules:
            if not rule.use_ast:
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
        
        # Deduplicate findings
        seen = set()
        unique_findings = []
        for f in findings:
            key = (f["rule"], f["line"], f["match"])
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)
        
        return unique_findings
    
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
