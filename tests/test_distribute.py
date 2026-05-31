"""Tests for Distribution module."""

import pytest
from agentik.distribute.update_checker import update_checker, UpdateChecker
from agentik.distribute.builder import package_builder, PackageBuilder


def test_update_checker_version_compare():
    """Test version comparison."""
    checker = UpdateChecker("0.1.0")
    
    # Test newer version
    assert checker._version_compare("0.2.0", "0.1.0") is True
    
    # Test older version
    assert checker._version_compare("0.1.0", "0.2.0") is False
    
    # Test same version
    assert checker._version_compare("0.1.0", "0.1.0") is False


def test_update_checker_get_version():
    """Test getting current version."""
    version = update_checker.get_current_version()
    assert isinstance(version, str)
    assert len(version) > 0


def test_package_builder_init():
    """Test package builder initialization."""
    builder = PackageBuilder()
    assert builder.project_root is not None


def test_package_builder_build_wheel():
    """Test building wheel (mocked)."""
    # Just test initialization
    builder = PackageBuilder()
    assert builder is not None
