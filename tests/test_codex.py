"""Tests for Codex module."""

import pytest
from agentik.native.codex import codex
from agentik.native.call_graph import call_graph_builder
from agentik.native.impact import impact_analyzer


def test_codex_parse_code():
    """Test parsing Python code."""
    code = """
def hello():
    print("hello")

class MyClass:
    def method(self):
        pass
"""
    result = codex.parse_code(code)
    assert result is not None
    assert result.node_type == "Module"


def test_codex_get_functions():
    """Test getting functions from code."""
    code = """
def hello():
    print("hello")

def world():
    print("world")
"""
    functions = codex.get_functions(code)
    assert len(functions) == 2
    assert functions[0]["name"] == "hello"
    assert functions[1]["name"] == "world"


def test_codex_get_classes():
    """Test getting classes from code."""
    code = """
class MyClass:
    def method(self):
        pass
"""
    classes = codex.get_classes(code)
    assert len(classes) == 1
    assert classes[0]["name"] == "MyClass"
    assert "method" in classes[0]["methods"]


def test_call_graph_build():
    """Test building call graph."""
    code = """
def a():
    b()

def b():
    c()

def c():
    pass
"""
    graph = call_graph_builder.build_from_code(code)
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2


def test_call_graph_callers():
    """Test getting callers."""
    code = """
def a():
    b()

def b():
    pass
"""
    graph = call_graph_builder.build_from_code(code)
    callers = call_graph_builder.get_callers(graph, "b")
    assert "a" in callers


def test_call_graph_callees():
    """Test getting callees."""
    code = """
def a():
    b()

def b():
    pass
"""
    graph = call_graph_builder.build_from_code(code)
    callees = call_graph_builder.get_callees(graph, "a")
    assert "b" in callees


def test_impact_analyzer():
    """Test impact analysis."""
    code = """
def a():
    b()

def b():
    pass
"""
    result = impact_analyzer.analyze(code, "b")
    assert result.symbol == "b"
    assert "a" in result.callers
    assert result.impact_level in ["low", "medium", "high", "critical"]
