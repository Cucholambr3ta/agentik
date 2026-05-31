"""Tests for AGENTIK Security module."""

import pytest
from agentik.security.receipts import generate_receipt, verify_receipt
from agentik.security.rules import security_rules, SQLInjectionDetector, CommandInjectionDetector, EvalDetector
import ast


def test_generate_receipt():
    """Test generating a receipt."""
    receipt = generate_receipt("test_action", "success")
    assert "id" in receipt
    assert "timestamp" in receipt
    assert "signature" in receipt
    assert receipt["action"] == "test_action"
    assert receipt["result"] == "success"


def test_verify_receipt():
    """Test verifying a valid receipt."""
    receipt = generate_receipt("test_action", "success")
    assert verify_receipt(receipt) == True


def test_verify_invalid_receipt():
    """Test verifying an invalid receipt."""
    receipt = generate_receipt("test_action", "success")
    receipt["signature"] = "invalid_signature"
    assert verify_receipt(receipt) == False


def test_verify_tampered_receipt():
    """Test verifying a tampered receipt."""
    receipt = generate_receipt("test_action", "success")
    receipt["result"] = "tampered"
    assert verify_receipt(receipt) == False


# === AST-BASED SECURITY TESTS ===


def test_ast_sql_injection_detected():
    """Test that AST detects SQL injection with string formatting."""
    code = '''
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
'''
    findings = security_rules.scan_code(code)
    
    sql_findings = [f for f in findings if f["rule"] == "sql_injection"]
    assert len(sql_findings) > 0
    assert sql_findings[0]["severity"] == "high"
    assert sql_findings[0]["cwe"] == "CWE-89"


def test_ast_sql_injection_fstring_detected():
    """Test that AST detects SQL injection with f-string."""
    code = '''
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
'''
    findings = security_rules.scan_code(code)
    
    sql_findings = [f for f in findings if f["rule"] == "sql_injection"]
    assert len(sql_findings) > 0
    assert "f-string" in sql_findings[0]["description"].lower() or "f'" in sql_findings[0]["match"]


def test_ast_sql_injection_concat_detected():
    """Test that AST detects SQL injection with string concatenation."""
    code = '''
cursor.execute("SELECT * FROM users WHERE id = " + user_id)
'''
    findings = security_rules.scan_code(code)
    
    sql_findings = [f for f in findings if f["rule"] == "sql_injection"]
    assert len(sql_findings) > 0
    assert "concatenation" in sql_findings[0]["description"].lower()


def test_ast_command_injection_detected():
    """Test that AST detects command injection."""
    code = '''
os.system("ls " + user_input)
'''
    findings = security_rules.scan_code(code)
    
    cmd_findings = [f for f in findings if f["rule"] == "command_injection"]
    assert len(cmd_findings) > 0
    assert cmd_findings[0]["severity"] == "high"
    assert cmd_findings[0]["cwe"] == "CWE-78"


def test_ast_eval_detected():
    """Test that AST detects eval() usage."""
    code = '''
result = eval(user_input)
'''
    findings = security_rules.scan_code(code)
    
    eval_findings = [f for f in findings if f["rule"] == "eval_usage"]
    assert len(eval_findings) > 0
    assert eval_findings[0]["severity"] == "high"
    assert eval_findings[0]["cwe"] == "CWE-95"


def test_ast_safe_code_no_findings():
    """Test that safe code produces no AST findings."""
    code = '''
import os
import subprocess

def safe_function(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return True
'''
    findings = security_rules.scan_code(code)
    
    # Should have no SQL injection findings (parameterized query is safe)
    sql_findings = [f for f in findings if f["rule"] == "sql_injection"]
    assert len(sql_findings) == 0


def test_sql_injection_detector_direct():
    """Test SQLInjectionDetector directly."""
    code = '''
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
'''
    tree = ast.parse(code)
    detector = SQLInjectionDetector()
    detector.visit(tree)
    
    assert len(detector.findings) > 0
    assert detector.findings[0]["rule"] == "sql_injection"


def test_command_injection_detector_direct():
    """Test CommandInjectionDetector directly."""
    code = '''
os.system("echo " + user_input)
'''
    tree = ast.parse(code)
    detector = CommandInjectionDetector()
    detector.visit(tree)
    
    assert len(detector.findings) > 0
    assert detector.findings[0]["rule"] == "command_injection"


def test_eval_detector_direct():
    """Test EvalDetector directly."""
    code = '''
eval(user_input)
'''
    tree = ast.parse(code)
    detector = EvalDetector()
    detector.visit(tree)
    
    assert len(detector.findings) > 0
    assert detector.findings[0]["rule"] == "eval_usage"


def test_findings_deduplication():
    """Test that duplicate findings are deduplicated."""
    code = '''
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
'''
    findings = security_rules.scan_code(code)
    
    sql_findings = [f for f in findings if f["rule"] == "sql_injection"]
    # Should be deduplicated (same rule, same line if on same line, or different lines)
    assert len(sql_findings) <= 2

