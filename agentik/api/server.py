"""AGENTIK API — FastAPI server for REST/WebSocket endpoints."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from agentik.api.models import (
    ChatMessage, ChatResponse, PipelineRequest, PipelineResponse,
    HealthResponse, ImpactRequest, ImpactResponse, SecurityScanResponse,
    Skill, SkillRunRequest, SkillRunResponse, EventResponse, TaskResponse
)
from agentik.core.event_bus import Event, EventType, event_bus
from agentik.core.context_builder import context_builder
from agentik.core.orchestrator import orchestrator


# FastAPI app
app = FastAPI(
    title="AGENTIK API",
    description="Agente de desarrollo con X-DD como runtime de validación",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint."""
    # Build context
    context = context_builder.build(message.message)
    
    # Execute task
    result = await orchestrator.execute_task("chat", message.message)
    
    return ChatResponse(
        response=f"Received: {message.message}",
        timestamp=datetime.now().isoformat(),
        task_id=result.get("task_id"),
        context_summary=context.final_context
    )


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket chat endpoint for streaming."""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Build context
            context = context_builder.build(data)
            
            # Send response
            await websocket.send_json({
                "type": "message",
                "content": f"Echo: {data}",
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        pass


@app.post("/xdd/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest):
    """Run X-DD pipeline."""
    from agentik.core.pipeline import run_pipeline
    
    result = run_pipeline(request.pipeline_path)
    return PipelineResponse(
        pipeline=result.get("pipeline", ""),
        steps=result.get("steps", 0),
        passed=result.get("passed", False),
        duration=result.get("duration", 0.0),
        receipt=result.get("receipt")
    )


@app.get("/codex/impact", response_model=ImpactResponse)
async def get_impact(symbol: str, direction: str = "upstream"):
    """Get impact analysis for a symbol."""
    return ImpactResponse(
        symbol=symbol,
        callers=[],
        callees=[],
        impact_level="low"
    )


@app.post("/aegis/scan", response_model=SecurityScanResponse)
async def scan_security():
    """Run security scan."""
    from agentik.core.security_audit import security_auditor
    
    results = security_auditor.full_audit()
    return SecurityScanResponse(
        semgrep=results.get("semgrep"),
        gitleaks=results.get("gitleaks"),
        trivy=results.get("trivy"),
        nuclei=results.get("nuclei")
    )


@app.get("/skills", response_model=List[Skill])
async def list_skills():
    """List available skills."""
    return []


@app.post("/skills/run", response_model=SkillRunResponse)
async def run_skill(request: SkillRunRequest):
    """Run a skill."""
    return SkillRunResponse(
        skill=request.skill_name,
        status="executed",
        result={"message": f"Skill {request.skill_name} executed"}
    )


@app.get("/events", response_model=List[EventResponse])
async def list_events(event_type: Optional[str] = None):
    """List events."""
    if event_type:
        try:
            et = EventType(event_type)
            events = event_bus.get_history(et)
        except ValueError:
            events = event_bus.get_history()
    else:
        events = event_bus.get_history()
    
    return [
        EventResponse(
            event_type=e.event_type.value,
            data=e.data,
            timestamp=e.timestamp.isoformat()
        )
        for e in events[-100:]  # Last 100 events
    ]


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks():
    """List tasks."""
    return [
        TaskResponse(
            id=t["id"],
            name=t["name"],
            status=t["status"],
            timestamp=t["timestamp"]
        )
        for t in orchestrator.get_task_history()
    ]
