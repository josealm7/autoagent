"""
Agent Engine
Motor principal del agente. Usa LangChain con Groq y patrón ReAct.

Flujo:
1. Recibe objetivo del usuario
2. El LLM decide qué herramientas usar y en qué orden
3. Ejecuta las herramientas una a una
4. Razona sobre los resultados
5. Devuelve respuesta final + pasos realizados
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from app.core.config import get_settings
from app.models.schemas import AgentResponse, AgentStep
from app.tools import ALL_TOOLS, TOOL_NAMES
from app.services.memory import session_store

logger = logging.getLogger(__name__)
settings = get_settings()

UPLOAD_DIR = Path("./data/uploads")

SYSTEM_PROMPT = """Eres AutoAgent, un asistente empresarial inteligente que puede realizar tareas de forma autónoma.

Tienes acceso a estas herramientas:
- **search_docs**: Busca en documentos internos de la empresa (ChromaDB)
- **web_search**: Busca información actualizada en internet  
- **send_email**: Envía emails a clientes o compañeros
- **read_document**: Lee y analiza archivos PDF o DOCX subidos por el usuario
- **summarize**: Resume textos largos

INSTRUCCIONES:
1. Analiza el objetivo del usuario cuidadosamente
2. Decide qué herramientas necesitas y en qué orden
3. Si el usuario menciona un documento o archivo, usa read_document con el nombre exacto del archivo
4. Usa primero search_docs para información interna, luego web_search si no encuentras nada
5. Si el usuario pide enviar algo por email, hazlo después de tener la información
6. Responde SIEMPRE en español
7. Sé completo en tu respuesta final, no la cortes ni la abrevies
8. Si no puedes completar una tarea, explica por qué claramente

Recuerda el historial de conversación para dar respuestas coherentes."""


def get_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )


def build_agent_executor() -> AgentExecutor:
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, ALL_TOOLS, prompt)

    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=True,
        max_iterations=settings.max_iterations,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )


def _get_uploaded_files_context() -> str:
    """Devuelve un string con los archivos disponibles en la carpeta de uploads."""
    if not UPLOAD_DIR.exists():
        return ""
    files = [f.name for f in UPLOAD_DIR.iterdir()
             if f.is_file() and f.suffix.lower() in {".pdf", ".docx", ".txt", ".md"}]
    if not files:
        return ""
    files_list = ", ".join(files)
    return (
        f"\n\n[ARCHIVOS DISPONIBLES EN EL SISTEMA: {files_list}. "
        f"Si el usuario pide analizar un documento, usa read_document con el nombre exacto del archivo.]"
    )


async def run_agent(
    session_id: str,
    objective: str,
    company_id: str = "default",
) -> AgentResponse:

    history = session_store.get_history(session_id)
    steps: list[AgentStep] = []
    tools_used: list[str] = []

    try:
        executor = build_agent_executor()

        # Enriquecer el objetivo con los archivos disponibles para que el agente
        # sepa qué documentos puede leer directamente.
        files_context = _get_uploaded_files_context()
        enriched_objective = objective + files_context

        result = await executor.ainvoke({
            "input": enriched_objective,
            "chat_history": history,
        })

        answer = result.get("output", "No se pudo generar una respuesta.")

        # Procesar pasos intermedios
        for action, observation in result.get("intermediate_steps", []):
            tool_name = getattr(action, "tool", "unknown")

            if tool_name not in tools_used:
                tools_used.append(tool_name)

            steps.append(AgentStep(
                type="action",
                content=f"Usando herramienta: {tool_name}",
                tool=tool_name,
            ))
            obs_str = str(observation)
            steps.append(AgentStep(
                type="observation",
                content=obs_str[:1500] + ("..." if len(obs_str) > 1500 else ""),
                tool=tool_name,
            ))

        steps.append(AgentStep(type="answer", content=answer))

        # Guardar en historial
        session_store.add_turn(session_id, objective, answer)

        return AgentResponse(
            session_id=session_id,
            answer=answer,
            steps=steps,
            tools_used=tools_used,
            success=True,
        )

    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        error_msg = "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, inténtalo de nuevo."

        return AgentResponse(
            session_id=session_id,
            answer=error_msg,
            steps=steps,
            tools_used=tools_used,
            success=False,
            error=str(e),
        )
