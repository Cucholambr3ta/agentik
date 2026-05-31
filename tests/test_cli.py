"""Tests for AGENTIK CLI module."""

import pytest
from agentik.channels.cli import run_command


def test_run_command_echo():
    """Test running echo command."""
    result, exit_code = run_command("echo hello")
    assert result == "hello"
    assert exit_code == 0


def test_run_command_ls():
    """Test running ls command."""
    result, exit_code = run_command("ls /")
    assert "home" in result or "usr" in result
    assert exit_code == 0


def test_run_command_invalid():
    """Test running invalid command."""
    result, exit_code = run_command("invalid_command_12345")
    assert "ERROR" in result or result == ""
    assert exit_code != 0
