"""AGENTIK Self-improvement — Main module for self-improve command."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from agentik.improve.patcher import patcher, Patch
from agentik.improve.validator import validator, ValidationResult


@dataclass
class ImprovementOpportunity:
    """Improvement opportunity."""
    id: str
    description: str
    file_path: str
    current_code: str
    suggested_code: str
    priority: str


class SelfImprover:
    """Self-improvement system."""
    
    def __init__(self):
        self._opportunities: List[ImprovementOpportunity] = []
    
    def detect_opportunities(self, code: str, file_path: str) -> List[ImprovementOpportunity]:
        """Detect improvement opportunities in code."""
        opportunities = []
        
        # Simple heuristics for improvement
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Check for TODO comments
            if 'TODO' in line or 'FIXME' in line:
                opportunities.append(ImprovementOpportunity(
                    id=f"opp-{len(opportunities)}",
                    description=f"TODO/FIXME found: {line.strip()}",
                    file_path=file_path,
                    current_code=line,
                    suggested_code="# " + line.strip(),
                    priority="medium"
                ))
            
            # Check for long lines
            if len(line) > 100:
                opportunities.append(ImprovementOpportunity(
                    id=f"opp-{len(opportunities)}",
                    description=f"Long line ({len(line)} chars)",
                    file_path=file_path,
                    current_code=line,
                    suggested_code=line[:100] + "...",
                    priority="low"
                ))
        
        self._opportunities.extend(opportunities)
        return opportunities
    
    def create_patch_from_opportunity(self, opportunity: ImprovementOpportunity) -> Patch:
        """Create a patch from an opportunity."""
        return patcher.create_patch(
            file_path=opportunity.file_path,
            original=opportunity.current_code,
            new=opportunity.suggested_code,
            description=opportunity.description
        )
    
    def apply_improvement(self, opportunity: ImprovementOpportunity) -> bool:
        """Apply an improvement."""
        patch = self.create_patch_from_opportunity(opportunity)
        
        # Validate the patch
        validation = validator.validate_patch(patch)
        
        if validation.overall:
            return patcher.apply_patch(patch)
        
        return False
    
    def get_opportunities(self) -> List[ImprovementOpportunity]:
        """Get all opportunities."""
        return self._opportunities.copy()


# Global self improver instance
self_improver = SelfImprover()
