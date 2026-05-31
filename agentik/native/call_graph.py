"""AGENTIK Codex — Call graph analysis."""

import ast
from typing import Any, Dict, List, Set, Optional
from dataclasses import dataclass, field


@dataclass
class CallEdge:
    """Call graph edge."""
    caller: str
    callee: str
    line: int


@dataclass
class CallGraph:
    """Call graph data structure."""
    edges: List[CallEdge] = field(default_factory=list)
    nodes: Set[str] = field(default_factory=set)


class CallGraphBuilder:
    """Build call graphs from Python code."""
    
    def __init__(self):
        self._graphs: Dict[str, CallGraph] = {}
    
    def build_from_code(self, code: str) -> CallGraph:
        """Build call graph from Python code."""
        graph = CallGraph()
        
        try:
            tree = ast.parse(code)
            self._visit_node(tree, graph)
        except SyntaxError:
            pass
        
        return graph
    
    def build_from_file(self, file_path: str) -> Optional[CallGraph]:
        """Build call graph from a Python file."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return self.build_from_code(code)
        except Exception:
            return None
    
    def _visit_node(self, node: ast.AST, graph: CallGraph, current_function: str = None):
        """Visit AST node recursively."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            current_function = node.name
            graph.nodes.add(current_function)
        
        elif isinstance(node, ast.ClassDef):
            graph.nodes.add(node.name)
            current_function = node.name
        
        elif isinstance(node, ast.Call):
            callee = self._get_call_name(node)
            if callee and current_function:
                graph.edges.append(CallEdge(
                    caller=current_function,
                    callee=callee,
                    line=getattr(node, 'lineno', 0)
                ))
                graph.nodes.add(callee)
        
        for child in ast.iter_child_nodes(node):
            self._visit_node(child, graph, current_function)
    
    def _get_call_name(self, node: ast.Call) -> Optional[str]:
        """Get the name of a function call."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None
    
    def get_callers(self, graph: CallGraph, function_name: str) -> List[str]:
        """Get all callers of a function."""
        return list(set(edge.caller for edge in graph.edges if edge.callee == function_name))
    
    def get_callees(self, graph: CallGraph, function_name: str) -> List[str]:
        """Get all callees of a function."""
        return list(set(edge.callee for edge in graph.edges if edge.caller == function_name))


# Global call graph builder instance
call_graph_builder = CallGraphBuilder()
