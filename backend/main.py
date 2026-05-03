import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api import agent, documents, health

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 55)
    logger.info("  AutoAgent API arrancando...")
    logger.info(f"  LLM     : {settings.llm_model}")
    logger.info(f"  Store   : {settings.vector_store}")
    logger.info(f"  Env     : {settings.app_env}")
    logger.info("=" * 55)
    Path("./data/chroma_db").mkdir(parents=True, exist_ok=True)
    Path("./data/uploads").mkdir(parents=True, exist_ok=True)
    yield
    logger.info("AutoAgent API apagándose...")


app = FastAPI(
    title="AutoAgent API",
    description="Agente IA empresarial con herramientas — LangChain + Groq",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(agent.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
