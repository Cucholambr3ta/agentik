"""Tests for Aegis module."""

import pytest
from agentik.security.rules import security_rules, SecurityRule, Severity
from agentik.security.aegis import aegis, AegisScanner


def test_security_rules_scan_code():
    """Test scanning code for vulnerabilities."""
    code = '''
password = "secret123"
os.system("rm -rf /")
'''
    findings = security_rules.scan_code(code)
    assert len(findings) > 0
    assert any(f["rule"] == "hardcoded_secret" for f in findings)
    assert any(f["rule"] == "command_injection" for f in findings)


def test_security_rules_no_vulnerabilities():
    """Test scanning safe code."""
    code = '''
x = 1
y = 2
print(x + y)
'''
    findings = security_rules.scan_code(code)
    assert len(findings) == 0


def test_aegis_scan_code():
    """Test Aegis scanning code."""
    code = '''
password = "secret123"
'''
    result = aegis.scan_code(code)
    assert result.total_findings > 0
    assert result.critical_count > 0


def test_aegis_scan_history():
    """Test scan history."""
    code = 'x = 1'
    aegis.scan_code(code)
    
    history = aegis.get_scan_history()
    assert len(history) > 0


def test_aegis_has_critical_findings():
    """Test checking for critical findings."""
    code = 'password = "secret123"'
    aegis.scan_code(code)
    
    assert aegis.has_critical_findings()
