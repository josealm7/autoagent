"""
Tool: summarize
Resume textos largos en puntos clave.
"""
from langchain_core.tools import tool


@tool
def summarize(text: str, style: str = "bullets") -> str:
    """
    Resume un texto largo en puntos clave.
    Úsala cuando tengas mucha información y necesites condensarla.
    Input: texto a resumir y estilo ('bullets' para lista, 'paragraph' para párrafo).
    """
    if not text or len(text.strip()) < 50:
        return "El texto es demasiado corto para resumir."

    # Limitar input
    if len(text) > 6000:
        text = text[:6000] + "..."

    if style == "bullets":
        instruction = "Resume el siguiente texto en 5-7 puntos clave con viñetas (•):"
    else:
        instruction = "Resume el siguiente texto en un párrafo conciso:"

    # Este tool devuelve instrucciones para el LLM, no llama a otra API
    return f"{instruction}\n\n{text}"
