from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import obtener_usuario_actual
from app.models.models import Usuario

from app.career.schemas_api import CareerRequest
from app.career.service import analizar_cv_vs_job

from app.career.cv_service import obtener_cv
from app.services.job_offer_service import obtener_oferta
from app.career.engine import analizar_ofertas_usuario
from app.models.models import OptimizedCV


router = APIRouter(
    prefix="/api/career",
    tags=["career"],
)


@router.post("/analyze")
def analyze(
    request: CareerRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):

    oferta = obtener_oferta(
        db=db,
        oferta_id=request.job_offer_id,
        usuario_id=usuario.id,
    )

    if not oferta:
        raise HTTPException(
            status_code=404,
            detail="Oferta no encontrada",
        )

    cv = obtener_cv(usuario.id)

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ningún CV para este usuario.",
        )

    job = f"""
Título:
{oferta.titulo}

Empresa:
{oferta.empresa}

Categoría:
{oferta.categoria}

Tags:
{oferta.tags}

Salario:
{oferta.salario}
"""

    resultado = analizar_cv_vs_job(
        cv=cv,
        job=job,
    )

    return resultado


@router.get("/rank-jobs")
def rank_jobs(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):

    resultados = analizar_ofertas_usuario(
        usuario.id,
        db,
    )

    return resultados

@router.get("/optimized-cv/{job_offer_id}")
def obtener_cv_optimizado(
    job_offer_id: int,
    db: Session = Depends(get_db),
):
    cv = db.query(OptimizedCV).filter_by(job_offer_id=job_offer_id).first()

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="Optimized CV not found",
        )

    return {
        "job_offer_id": cv.job_offer_id,
        "content": cv.content,
    }