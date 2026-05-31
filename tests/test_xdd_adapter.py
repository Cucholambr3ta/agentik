"""Tests for AGENTIK XDD Adapter module."""

import pytest
from agentik.channels.xdd_adapter import XDDAdapter


def test_xdd_adapter_init():
    """Test initializing XDDAdapter."""
    adapter = XDDAdapter()
    assert adapter.audit_log == []


def test_xdd_adapter_build_failure_when_xdd_missing():
    """Test that build returns failure when xdd is not installed."""
    adapter = XDDAdapter()
    result = adapter.build()
    
    # Should fail because xdd is not installed or command fails
    assert result["status"] == "failure"
    assert result["receipt"]["result"] == "failure"
    assert len(adapter.audit_log) == 1


def test_xdd_adapter_qa_review_failure_when_xdd_missing():
    """Test that qa_review returns failure when xdd is not installed."""
    adapter = XDDAdapter()
    result = adapter.qa_review()
    
    assert result["status"] == "failure"
    assert result["receipt"]["result"] == "failure"


def test_xdd_adapter_close_phase_failure_when_xdd_missing():
    """Test that close_phase returns failure when xdd is not installed."""
    adapter = XDDAdapter()
    result = adapter.close_phase()
    
    assert result["status"] == "failure"
    assert result["receipt"]["result"] == "failure"


def test_xdd_adapter_audit_log_appended():
    """Test that audit log is appended on failure."""
    adapter = XDDAdapter()
    
    adapter.build()
    adapter.qa_review()
    adapter.close_phase()
    
    assert len(adapter.audit_log) == 3


def test_xdd_adapter_receipt_has_required_fields():
    """Test that receipts have required fields."""
    adapter = XDDAdapter()
    result = adapter.build()
    
    receipt = result["receipt"]
    assert "action" in receipt
    assert "result" in receipt
    assert "signature" in receipt
    assert "timestamp" in receipt


def test_xdd_adapter_error_message_on_failure():
    """Test that error message is provided on failure."""
    adapter = XDDAdapter()
    result = adapter.build()
    
    assert "error" in result
    assert isinstance(result["error"], str)
