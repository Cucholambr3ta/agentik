"""Tests for Context Builder module."""

import pytest
from agentik.core.context_builder import ContextBuilder, Context


def test_context_builder_build():
    """Test building context."""
    builder = ContextBuilder()
    context = builder.build("Hello, world!")
    
    assert context.user_input == "Hello, world!"
    assert isinstance(context.conversation, list)
    assert isinstance(context.memories, list)
    assert isinstance(context.lessons, list)
    assert isinstance(context.skills, list)
    assert isinstance(context.security_policies, list)
    assert isinstance(context.final_context, dict)


def test_context_builder_conversation():
    """Test conversation context."""
    builder = ContextBuilder()
    
    builder.add_to_conversation("user", "Hello")
    builder.add_to_conversation("assistant", "Hi there!")
    
    context = builder.build("How are you?")
    assert len(context.conversation) == 2


def test_context_builder_security_policies():
    """Test security policies."""
    builder = ContextBuilder()
    context = builder.build("Test input")
    
    assert len(context.security_policies) > 0
    assert any(p["policy"] == "no_absolute_paths" for p in context.security_policies)


def test_context_builder_final_context():
    """Test final context structure."""
    builder = ContextBuilder()
    context = builder.build("Test input")
    
    assert "user_input" in context.final_context
    assert "conversation_length" in context.final_context
    assert "timestamp" in context.final_context
