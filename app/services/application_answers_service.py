import json

from app.models.models import ApplicationAnswers


def guardar_application_answers(
    db,
    job_offer_id,
    respuestas_json,
):
    respuestas = json.loads(respuestas_json)

    existente = (
        db.query(ApplicationAnswers)
        .filter(
            ApplicationAnswers.job_offer_id == job_offer_id
        )
        .first()
    )

    if existente:
        existente.tell_me_about_yourself = respuestas["tell_me_about_yourself"]
        existente.why_this_company = respuestas["why_this_company"]
        existente.why_should_we_hire_you = respuestas["why_should_we_hire_you"]
        existente.greatest_strength = respuestas["greatest_strength"]
        existente.greatest_weakness = respuestas["greatest_weakness"]
        db.commit()
        return existente

    nuevo = ApplicationAnswers(
        job_offer_id=job_offer_id,
        tell_me_about_yourself=respuestas["tell_me_about_yourself"],
        why_this_company=respuestas["why_this_company"],
        why_should_we_hire_you=respuestas["why_should_we_hire_you"],
        greatest_strength=respuestas["greatest_strength"],
        greatest_weakness=respuestas["greatest_weakness"],
    )

    db.add(nuevo)
    db.commit()

    return nuevo