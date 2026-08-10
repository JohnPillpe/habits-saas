import json

from app.models.models import InterviewPreparation


def guardar_interview_preparation(
    db,
    job_offer_id,
    preparation_json,
):

    data = json.loads(preparation_json)

    required_keys = [
        "technical_questions",
        "behavioral_questions",
        "tips",
    ]

    for key in required_keys:
        if key not in data:
            raise ValueError(
                f"Interview preparation missing key: {key}"
            )

    existente = (
        db.query(InterviewPreparation)
        .filter(
            InterviewPreparation.job_offer_id == job_offer_id
        )
        .first()
    )

    if existente:

        existente.technical_questions = data["technical_questions"]
        existente.behavioral_questions = data["behavioral_questions"]
        existente.tips = data["tips"]

        db.commit()

        return existente

    nuevo = InterviewPreparation(
        job_offer_id=job_offer_id,
        technical_questions=data["technical_questions"],
        behavioral_questions=data["behavioral_questions"],
        tips=data["tips"],
    )

    db.add(nuevo)
    db.commit()

    return nuevo