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


# === REAL LOGIC TESTS ===


def test_context_builder_pipeline_order():
    """Test that context builder follows spec pipeline order."""
    call_order = []
    
    builder = ContextBuilder()
    
    # Track call order by checking final_context
    original_get_conversation = builder._get_conversation_context
    original_get_memories = builder._get_relevant_memories
    original_get_lessons = builder._get_relevant_lessons
    original_get_skills = builder._get_relevant_skills
    original_get_security = builder._get_security_policies
    
    def track_conversation(user_input):
        call_order.append("conversation")
        return original_get_conversation(user_input)
    
    def track_memories(user_input):
        call_order.append("memories")
        return original_get_memories(user_input)
    
    def track_lessons(user_input):
        call_order.append("lessons")
        return original_get_lessons(user_input)
    
    def track_skills(user_input):
        call_order.append("skills")
        return original_get_skills(user_input)
    
    def track_security(user_input):
        call_order.append("security")
        return original_get_security(user_input)
    
    builder._get_conversation_context = track_conversation
    builder._get_relevant_memories = track_memories
    builder._get_relevant_lessons = track_lessons
    builder._get_relevant_skills = track_skills
    builder._get_security_policies = track_security
    
    builder.build("Test input")
    
    # Pipeline order: conversation → memories → lessons → skills → security
    assert call_order == ["conversation", "memories", "lessons", "skills", "security"]


def test_context_builder_empty_input():
    """Test building context with empty input."""
    builder = ContextBuilder()
    context = builder.build("")
    
    assert context.user_input == ""
    assert context.final_context["user_input"] == ""


def test_context_builder_conversation_limit():
    """Test that conversation context is limited to 10 messages."""
    builder = ContextBuilder()
    
    # Add 15 messages
    for i in range(15):
        builder.add_to_conversation("user", f"Message {i}")
    
    context = builder.build("New message")
    
    # Should only keep last 10
    assert len(context.conversation) == 10
    assert context.conversation[0]["content"] == "Message 5"
    assert context.conversation[-1]["content"] == "Message 14"

