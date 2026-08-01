from app.models.models import CoverLetter


def guardar_cover_letter(
    db,
    job_offer_id,
    content,
):
    existente = (
        db.query(CoverLetter)
        .filter(
            CoverLetter.job_offer_id == job_offer_id
        )
        .first()
    )

    if existente:
        existente.content = content
        db.commit()
        return existente

    nuevo = CoverLetter(
        job_offer_id=job_offer_id,
        content=content,
    )

    db.add(nuevo)
    db.commit()

    return nuevo