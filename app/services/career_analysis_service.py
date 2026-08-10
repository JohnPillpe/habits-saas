from app.models.models import CareerAnalysis, JobOffer


def guardar_analisis(db, job_offer_id, analisis):

    registro = (
        db.query(CareerAnalysis)
        .filter(CareerAnalysis.job_offer_id == job_offer_id)
        .first()
    )

    if not registro:
        registro = CareerAnalysis(job_offer_id=job_offer_id)
        db.add(registro)

    registro.match_score = analisis["match_score"]

    registro.candidate_summary = analisis["summary"]
    registro.job_summary = ""

    registro.strengths = analisis["strengths"]
    registro.missing_skills = analisis["missing_skills"]
    registro.improvements = analisis["next_steps"]

    job = (
        db.query(JobOffer)
        .filter(JobOffer.id == job_offer_id)
        .first()
    )

    if job:
        job.match_score = analisis["match_score"]

    db.commit()

    return registro