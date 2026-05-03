from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
from app.models.schemas import IngestResponse
from app.services.ingestion import ingest_files, get_store
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("./data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


@router.post("/upload", response_model=IngestResponse)
async def upload_documents(
    files: list[UploadFile] = File(...),
):
    saved_paths: list[Path] = []
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    for file in files:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400,
                                detail=f"Tipo no soportado: {file.filename}")
        dest = UPLOAD_DIR / file.filename
        dest.write_bytes(await file.read())
        saved_paths.append(dest)

    try:
        chunks, processed = await ingest_files(saved_paths)
        return IngestResponse(status="ok", chunks_indexed=chunks,
                              files_processed=processed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/count")
async def get_count():
    try:
        store = get_store()
        return {"chunks": store._collection.count()}
    except Exception:
        return {"chunks": 0}
