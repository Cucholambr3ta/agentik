"""Tests for AGENTIK XDD Adapter module."""

import pytest
from agentik.channels.xdd_adapter import XDDAdapter


def test_xdd_adapter_init():
    """Test initializing XDDAdapter."""
    adapter = XDDAdapter()
    assert adapter.audit_log == []


def test_xdd_adapter_build():
    """Test build method."""
    adapter = XDDAdapter()
    result = adapter.build()
    assert result["status"] == "success"
    assert len(adapter.audit_log) == 1


def test_xdd_adapter_qa_review():
    """Test qa_review method."""
    adapter = XDDAdapter()
    result = adapter.qa_review()
    assert result["status"] == "success"
    assert len(adapter.audit_log) == 1


def test_xdd_adapter_close_phase():
    """Test close_phase method."""
    adapter = XDDAdapter()
    result = adapter.close_phase()
    assert result["status"] == "success"
    assert len(adapter.audit_log) == 1
