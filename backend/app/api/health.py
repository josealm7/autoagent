from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.ingestion import get_store
from app.services.memory import session_store
from app.tools import TOOL_NAMES
from app.core.config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health():
    try:
        store = get_store()
        count = store._collection.count()
    except Exception:
        count = -1

    return HealthResponse(
        status="ok",
        vector_store=settings.vector_store,
        documents_indexed=count,
        agent_tools=TOOL_NAMES,
    )


@router.get("/")
async def root():
    return {
        "name": "AutoAgent API",
        "version": "1.0.0",
        "docs": "/docs",
        "tools": TOOL_NAMES,
        "active_sessions": session_store.active_sessions,
    }
