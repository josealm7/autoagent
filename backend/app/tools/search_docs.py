"""
Tool: search_docs
Busca información en los documentos indexados de la empresa (ChromaDB).
Comparte la misma base vectorial que SmartChat.
"""
from langchain_core.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()

_embeddings = None
_store = None


def _get_store():
    global _embeddings, _store
    if _store is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        persist_dir = Path(settings.chroma_persist_dir) / "default"
        persist_dir.mkdir(parents=True, exist_ok=True)
        _store = Chroma(
            collection_name="smartchat_default",
            embedding_function=_embeddings,
            persist_directory=str(persist_dir),
        )
    return _store


@tool
def search_docs(query: str) -> str:
    """
    Busca información relevante en los documentos internos de la empresa.
    Úsala cuando necesites información sobre productos, precios, políticas o procedimientos internos.
    Input: pregunta o tema a buscar.
    """
    try:
        store = _get_store()
        results = store.similarity_search_with_relevance_scores(
            query, k=settings.retrieval_k
        )
        relevant = [(doc, score) for doc, score in results
                    if score >= settings.similarity_threshold]

        if not relevant:
            return "No encontré información relevante en los documentos internos sobre ese tema."

        parts = []
        for i, (doc, score) in enumerate(relevant, 1):
            src = doc.metadata.get("source_file", "documento")
            parts.append(f"[Fuente {i} - {src}]:\n{doc.page_content.strip()}")

        return "\n\n".join(parts)
    except Exception as e:
        return f"Error al buscar en documentos: {str(e)}"
