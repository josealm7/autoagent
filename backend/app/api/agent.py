from fastapi import APIRouter, HTTPException
from app.models.schemas import AgentRequest, AgentResponse
from app.services.agent_engine import run_agent
from app.services.memory import session_store
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("", response_model=AgentResponse)
async def run_agent_endpoint(req: AgentRequest):
    """
    Ejecuta el agente con un objetivo.
    El agente decide qué herramientas usar y las ejecuta automáticamente.
    """
    try:
        return await run_agent(
            session_id=req.session_id,
            objective=req.objective,
            company_id=req.company_id,
        )
    except Exception as e:
        logger.error(f"Agent endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    session_store.clear_session(session_id)
    return {"status": "ok", "session_id": session_id}
