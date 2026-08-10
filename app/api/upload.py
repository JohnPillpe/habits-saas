from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.models import Usuario, Document
from app.rag.vector_store import guardar_fragmentos

from app.rag.vector_store import get_collection


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def dividir_texto(
    texto: str,
    tamano: int = 1500,
    solapamiento: int = 200,
):
    """
    Divide el CV en fragmentos para almacenarlos
    en ChromaDB.
    """

    texto = texto.strip()

    if not texto:
        return []

    fragmentos = []

    inicio = 0
    longitud = len(texto)

    while inicio < longitud:

        fin = inicio + tamano

        fragmento = texto[inicio:fin].strip()

        if fragmento:
            fragmentos.append(fragmento)

        inicio = fin - solapamiento

    return fragmentos


@router.post("/cv")
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    # -----------------------------------
    # 1. SAVE PDF
    # -----------------------------------

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    # -----------------------------------
    # 2. EXTRACT TEXT
    # -----------------------------------

    reader = PdfReader(destination)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    text = text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF",
        )

    # -----------------------------------
    # 3. SAVE DOCUMENT
    # -----------------------------------

    document = Document(
        usuario_id=usuario.id,
        nombre=file.filename,
        tipo="cv",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # -----------------------------------
    # 4. SPLIT CV
    # -----------------------------------

    fragmentos = dividir_texto(text)

    # -----------------------------------
    # 5. SAVE CV IN CHROMADB
    # -----------------------------------

    guardar_fragmentos(
        usuario_id=usuario.id,
        nombre_documento=file.filename,
        fragmentos=fragmentos,
    )

    # -----------------------------------
    # 6. RESPONSE
    # -----------------------------------

    return {
        "document_id": document.id,
        "filename": file.filename,
        "characters": len(text),
        "fragments": len(fragmentos),
        "preview": text[:500],
        "message": "CV uploaded successfully",
    }


@router.get("/has-cv")
def has_cv(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    collection = get_collection()

    resultados = collection.get(
        where={"usuario_id": usuario.id},
        include=["documents", "metadatas"],
    )

    documentos = resultados.get("documents", [])

    return {
        "has_cv": len(documentos) > 0
    }

