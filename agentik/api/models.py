"""AGENTIK API Models — Pydantic models for API endpoints."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    user_id: str = "anonymous"
    timestamp: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    timestamp: str
    task_id: Optional[str] = None
    context_summary: Optional[Dict[str, Any]] = None


class PipelineRequest(BaseModel):
    """Pipeline request model."""
    pipeline_path: str


class PipelineResponse(BaseModel):
    """Pipeline response model."""
    pipeline: str
    steps: int
    passed: bool
    duration: float
    receipt: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    timestamp: str


class ImpactRequest(BaseModel):
    """Impact analysis request model."""
    symbol: str
    direction: str = "upstream"


class ImpactResponse(BaseModel):
    """Impact analysis response model."""
    symbol: str
    callers: List[str]
    callees: List[str]
    impact_level: str


class SecurityScanResponse(BaseModel):
    """Security scan response model."""
    semgrep: Optional[Dict[str, Any]] = None
    gitleaks: Optional[Dict[str, Any]] = None
    trivy: Optional[Dict[str, Any]] = None
    nuclei: Optional[Dict[str, Any]] = None


class Skill(BaseModel):
    """Skill model."""
    name: str
    description: str
    version: str = "0.1.0"


class SkillRunRequest(BaseModel):
    """Skill run request model."""
    skill_name: str
    params: Dict[str, Any] = {}


class SkillRunResponse(BaseModel):
    """Skill run response model."""
    skill: str
    status: str
    result: Optional[Dict[str, Any]] = None


class EventResponse(BaseModel):
    """Event response model."""
    event_type: str
    data: Dict[str, Any]
    timestamp: str


class TaskResponse(BaseModel):
    """Task response model."""
    id: str
    name: str
    status: str
    timestamp: str
