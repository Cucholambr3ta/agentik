"""Tests for AGENTIK Security module."""

import pytest
from agentik.security.receipts import generate_receipt, verify_receipt


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
