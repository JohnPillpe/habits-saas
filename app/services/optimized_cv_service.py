from app.models.models import OptimizedCV


def guardar_cv_optimizado(
    db,
    job_offer_id,
    content,
):
    existente = (
        db.query(OptimizedCV)
        .filter(
            OptimizedCV.job_offer_id == job_offer_id
        )
        .first()
    )

    if existente:
        existente.content = content
        db.commit()
        return existente

    nuevo = OptimizedCV(
        job_offer_id=job_offer_id,
        content=content,
    )

    db.add(nuevo)
    db.commit()

    return nuevo