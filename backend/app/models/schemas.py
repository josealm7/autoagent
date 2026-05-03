from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# ── Agent Run ─────────────────────────────────────────────────────────────────

class AgentStep(BaseModel):
    """Un paso del razonamiento del agente."""
    type: Literal["thought", "action", "observation", "answer"]
    content: str
    tool: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentRequest(BaseModel):
    session_id: str
    objective: str = Field(..., min_length=1, max_length=2000,
                           description="Objetivo o tarea para el agente")
    company_id: str = Field(default="default")


class AgentResponse(BaseModel):
    session_id: str
    answer: str
    steps: list[AgentStep] = []
    tools_used: list[str] = []
    success: bool = True
    error: Optional[str] = None


# ── Documents ─────────────────────────────────────────────────────────────────

class IngestResponse(BaseModel):
    status: str
    chunks_indexed: int
    files_processed: list[str]


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    vector_store: str
    documents_indexed: int
    agent_tools: list[str]
    version: str = "1.0.0"
