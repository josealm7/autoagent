"""
Tool: read_pdf
Lee y extrae texto de archivos PDF subidos.
"""
from langchain_core.tools import tool
from pathlib import Path


@tool
def read_pdf(file_path: str) -> str:
    """
    Lee y extrae el contenido de un archivo PDF.
    Úsala cuando el usuario suba un PDF y pida analizarlo, resumirlo o extraer información.
    Input: ruta al archivo PDF.
    """
    try:
        from pypdf import PdfReader

        path = Path(file_path)
        if not path.exists():
            return f"No se encontró el archivo: {file_path}"

        if path.suffix.lower() != ".pdf":
            return f"El archivo no es un PDF: {file_path}"

        reader = PdfReader(str(path))
        pages_text = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                pages_text.append(f"[Página {i+1}]\n{text.strip()}")

        if not pages_text:
            return "El PDF no contiene texto extraíble (puede ser un PDF escaneado)."

        full_text = "\n\n".join(pages_text)

        # Limitar a 4000 caracteres para no saturar el contexto
        if len(full_text) > 4000:
            full_text = full_text[:4000] + "\n\n[... texto truncado ...]"

        return full_text

    except Exception as e:
        return f"Error al leer PDF: {str(e)}"
