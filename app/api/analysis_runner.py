from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.models import Usuario

from app.career.engine import analizar_oferta_usuario


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post("/{job_offer_id}")
def run_single_analysis(
    job_offer_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    resultado = analizar_oferta_usuario(
        usuario.id,
        job_offer_id,
        db,
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer or CV not found",
        )

    return resultado["analisis"]