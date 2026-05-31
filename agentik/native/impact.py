"""AGENTIK Codex — Impact analysis."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from agentik.native.codex import codex
from agentik.native.call_graph import call_graph_builder, CallGraph


@dataclass
class ImpactResult:
    """Impact analysis result."""
    symbol: str
    callers: List[str]
    callees: List[str]
    impact_level: str  # low, medium, high, critical
    affected_files: List[str]


class ImpactAnalyzer:
    """Analyze impact of changing a symbol."""
    
    def __init__(self):
        self._cache: Dict[str, ImpactResult] = {}
    
    def analyze(self, code: str, symbol: str) -> ImpactResult:
        """Analyze impact of changing a symbol in code."""
        graph = call_graph_builder.build_from_code(code)
        
        callers = call_graph_builder.get_callers(graph, symbol)
        callees = call_graph_builder.get_callees(graph, symbol)
        
        # Calculate impact level
        impact_level = self._calculate_impact_level(callers, callees)
        
        return ImpactResult(
            symbol=symbol,
            callers=callers,
            callees=callees,
            impact_level=impact_level,
            affected_files=[]
        )
    
    def analyze_file(self, file_path: str, symbol: str) -> Optional[ImpactResult]:
        """Analyze impact of changing a symbol in a file."""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return self.analyze(code, symbol)
        except Exception:
            return None
    
    def _calculate_impact_level(self, callers: List[str], callees: List[str]) -> str:
        """Calculate impact level based on callers and callees."""
        total = len(callers) + len(callees)
        
        if total == 0:
            return "low"
        elif total <= 3:
            return "medium"
        elif total <= 7:
            return "high"
        else:
            return "critical"


# Global impact analyzer instance
impact_analyzer = ImpactAnalyzer()
