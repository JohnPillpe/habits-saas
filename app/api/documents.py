from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.models import Usuario


from app.rag.processor import (
    extraer_texto_pdf,
    dividir_en_fragmentos,
)

from app.rag.vector_store import guardar_fragmentos
from app.services.document_service import guardar_documento
from app.services.document_service import listar_documentos

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF",
        )

    try:

        contenido = await file.read()

        texto = extraer_texto_pdf(contenido)

        if not texto.strip():
            raise HTTPException(
                status_code=400,
                detail="El PDF no contiene texto",
            )

        fragmentos = dividir_en_fragmentos(
            texto,
            tamano_chunk=500,
        )

        if not fragmentos:
            raise HTTPException(
                status_code=400,
                detail="No se pudieron generar fragmentos",
            )

        guardar_documento(
            db=db,
            usuario_id=usuario.id,
            nombre=file.filename,
            tipo=file.filename.split(".")[-1].lower(),
        )

        guardar_fragmentos(
            usuario_id=usuario.id,
            nombre_documento=file.filename,
            fragmentos=fragmentos,
        )

    
        return {
            "message": f"Documento '{file.filename}' procesado correctamente.",
            "fragmentos_guardados": len(fragmentos),
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.get("/")
def obtener_documentos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    documentos = listar_documentos(
        db=db,
        usuario_id=usuario.id,
    )

    return [
        {
            "id": d.id,
            "nombre": d.nombre,
            "tipo": d.tipo,
            "fecha_subida": d.fecha_subida,
        }
        for d in documentos
    ]