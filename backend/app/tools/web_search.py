"""
Tool: web_search
Busca información actualizada en internet usando DuckDuckGo.
Gratis, sin API key necesaria.
"""
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Busca información actualizada en internet.
    Úsala cuando no encuentres la respuesta en los documentos internos,
    o cuando necesites información reciente, precios de competencia, noticias, etc.
    Input: término o pregunta a buscar.
    """
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))

        if not results:
            return "No encontré resultados en internet para esa búsqueda."

        parts = []
        for r in results:
            title = r.get("title", "Sin título")
            body = r.get("body", "")
            href = r.get("href", "")
            parts.append(f"**{title}**\n{body}\nFuente: {href}")

        return "\n\n---\n\n".join(parts)

    except Exception as e:
        return f"Error en búsqueda web: {str(e)}"
