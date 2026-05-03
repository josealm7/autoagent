"""
Tool: read_document
Lee y extrae texto de archivos PDF o DOCX subidos.
"""
from langchain_core.tools import tool
from pathlib import Path

UPLOAD_DIR = Path("./data/uploads")
MAX_CHARS = 8000


@tool
def read_document(file_path: str) -> str:
    """
    Lee y extrae el contenido de un archivo PDF o DOCX.
    Úsala cuando el usuario suba un documento (PDF o Word/DOCX) y pida analizarlo,
    resumirlo o extraer información.
    Input: nombre del archivo o ruta completa. Si solo se da el nombre, se busca
    automáticamente en la carpeta de uploads.
    """
    try:
        path = Path(file_path)

        # Si no existe como ruta absoluta, buscar en UPLOAD_DIR
        if not path.exists():
            candidate = UPLOAD_DIR / path.name
            if candidate.exists():
                path = candidate
            else:
                # Intentar encontrar el archivo por nombre parcial
                matches = list(UPLOAD_DIR.glob(f"*{path.name}*"))
                if matches:
                    path = matches[0]
                else:
                    # Listar archivos disponibles para ayudar al agente
                    available = [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()]
                    if available:
                        return (
                            f"No se encontró '{file_path}'. "
                            f"Archivos disponibles: {', '.join(available)}"
                        )
                    return f"No se encontró el archivo '{file_path}' y no hay archivos subidos."

        ext = path.suffix.lower()

        if ext == ".pdf":
            return _read_pdf(path)
        elif ext == ".docx":
            return _read_docx(path)
        else:
            return f"Formato no soportado: {ext}. Usa archivos PDF o DOCX."

    except Exception as e:
        return f"Error al leer el documento: {str(e)}"


def _read_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages_text = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages_text.append(f"[Página {i + 1}]\n{text.strip()}")

    if not pages_text:
        return "El PDF no contiene texto extraíble (puede ser un PDF escaneado o de solo imágenes)."

    full_text = "\n\n".join(pages_text)
    return _truncate(full_text, path.name)


def _read_docx(path: Path) -> str:
    from docx import Document as DocxDocument

    doc = DocxDocument(str(path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    if not paragraphs:
        return "El archivo DOCX no contiene texto extraíble."

    full_text = "\n\n".join(paragraphs)
    return _truncate(full_text, path.name)


def _truncate(text: str, filename: str) -> str:
    header = f"[Archivo: {filename}]\n\n"
    if len(text) > MAX_CHARS:
        return header + text[:MAX_CHARS] + f"\n\n[... texto truncado. Total: {len(text)} caracteres ...]"
    return header + text
