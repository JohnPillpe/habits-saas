from sqlalchemy.orm import Session

from app.models.models import JobOffer


def obtener_oferta(
    db: Session,
    oferta_id: int,
    usuario_id: int,
):
    return (
        db.query(JobOffer)
        .filter(
            JobOffer.id == oferta_id,
            JobOffer.usuario_id == usuario_id,
        )
        .first()
    )