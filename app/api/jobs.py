from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Usuario, JobOffer
from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/job-offers", tags=["Jobs"])

@router.get("/job-offers")
def listar_ofertas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    ofertas = db.query(JobOffer).filter(
        JobOffer.usuario_id == usuario.id
    ).all()

    return ofertas