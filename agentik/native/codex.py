"""AGENTIK Codex — AST analysis with tree-sitter."""

import ast
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ASTNode:
    """AST node data structure."""
    name: str
    node_type: str
    line: int
    col: int
    children: List['ASTNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class CodexAnalyzer:
    """AST analysis for Python code using tree-sitter."""
    
    def __init__(self):
        self._cache: Dict[str, ASTNode] = {}
    
    def parse_file(self, file_path: str) -> Optional[ASTNode]:
        """Parse a Python file and return AST."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return self.parse_code(content)
        except Exception as e:
            return None
    
    def parse_code(self, code: str) -> Optional[ASTNode]:
        """Parse Python code and return AST."""
        try:
            tree = ast.parse(code)
            return self._visit_node(tree)
        except SyntaxError:
            return None
    
    def _visit_node(self, node: ast.AST) -> ASTNode:
        """Visit an AST node recursively."""
        children = []
        for child in ast.iter_child_nodes(node):
            children.append(self._visit_node(child))
        
        return ASTNode(
            name=getattr(node, 'name', getattr(node, 'id', '')),
            node_type=type(node).__name__,
            line=getattr(node, 'lineno', 0),
            col=getattr(node, 'col_offset', 0),
            children=children
        )
    
    def get_functions(self, code: str) -> List[Dict[str, Any]]:
        """Get all functions from code."""
        try:
            tree = ast.parse(code)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [self._get_decorator_name(d) for d in node.decorator_list]
                    })
            
            return functions
        except SyntaxError:
            return []
    
    def get_classes(self, code: str) -> List[Dict[str, Any]]:
        """Get all classes from code."""
        try:
            tree = ast.parse(code)
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "bases": [self._get_base_name(b) for b in node.bases],
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
            
            return classes
        except SyntaxError:
            return []
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{self._get_base_name(decorator.value)}.{decorator.attr}"
        return str(decorator)
    
    def _get_base_name(self, base: ast.AST) -> str:
        """Get base class name."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{self._get_base_name(base.value)}.{base.attr}"
        return str(base)


# Global codex analyzer instance
codex = CodexAnalyzer()
