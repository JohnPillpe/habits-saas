from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Usuario, JobOffer
from app.core.auth import get_current_user

router = APIRouter(prefix="/job-offers", tags=["Jobs"])

@router.get("")
def listar_ofertas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    ofertas = db.query(JobOffer).filter(
        JobOffer.usuario_id == usuario.id
    ).all()

    return ofertas