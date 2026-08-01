from app.models.models import CareerAnalysis


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
    registro.candidate_summary = analisis["candidate_summary"]
    registro.job_summary = analisis["job_summary"]
    registro.strengths = analisis["strengths"]
    registro.missing_skills = analisis["missing_skills"]
    registro.improvements = analisis["improvements"]

    db.commit()

    return registro