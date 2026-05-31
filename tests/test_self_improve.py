"""Tests for Self-improvement module."""

import pytest
import tempfile
import os
from agentik.improve.patcher import patcher, Patcher, Patch
from agentik.improve.validator import validator, Validator
from agentik.improve.self import self_improver, SelfImprover


def test_patcher_create_patch():
    """Test creating a patch."""
    patch = patcher.create_patch(
        file_path="test.py",
        original="old code",
        new="new code",
        description="test patch"
    )
    assert patch is not None
    assert patch.file_path == "test.py"


def test_patcher_generate_diff():
    """Test generating diff."""
    patch = patcher.create_patch(
        file_path="test.py",
        original="old line",
        new="new line",
        description="test"
    )
    diff = patcher.generate_diff(patch)
    assert "old line" in diff
    assert "new line" in diff


def test_patcher_get_patches():
    """Test getting patches."""
    patcher.create_patch("test.py", "old", "new", "test")
    patches = patcher.get_patches()
    assert len(patches) > 0


def test_validator_validate_patch():
    """Test validating a patch."""
    patch = patcher.create_patch(
        file_path="test.py",
        original="old",
        new="new",
        description="test"
    )
    result = validator.validate_patch(patch)
    assert result is not None
    assert hasattr(result, 'overall')


def test_self_improver_detect_opportunities():
    """Test detecting opportunities."""
    code = '''
# TODO: fix this
x = 1
'''
    opportunities = self_improver.detect_opportunities(code, "test.py")
    assert len(opportunities) > 0


def test_self_improver_get_opportunities():
    """Test getting opportunities."""
    code = '''
# TODO: fix this
# FIXME: another issue
'''
    self_improver.detect_opportunities(code, "test.py")
    opportunities = self_improver.get_opportunities()
    assert len(opportunities) > 0
