from collections import Counter

from app.models.models import CareerAnalysis, JobOffer


def obtener_dashboard(db):

    analisis = db.query(CareerAnalysis).all()

    if not analisis:
        return {
            "total_jobs": 0,
            "average_match": 0,
            "best_match": 0,
            "top_jobs": [],
            "top_missing_skills": [],
        }

    total = len(analisis)

    promedio = sum(a.match_score for a in analisis) / total

    mejor = max(a.match_score for a in analisis)

    top_jobs = (
        db.query(CareerAnalysis, JobOffer)
        .join(JobOffer, CareerAnalysis.job_offer_id == JobOffer.id)
        .order_by(CareerAnalysis.match_score.desc())
        .limit(5)
        .all()
    )

    skill_counter = Counter()

    for analysis in analisis:
        for skill in analysis.missing_skills:
            skill_counter[skill] += 1

    top_missing_skills = [
        {
            "skill": skill,
            "count": count,
        }
        for skill, count in skill_counter.most_common(5)
    ]

    return {
        "total_jobs": total,
        "average_match": round(promedio),
        "best_match": mejor,
        "top_jobs": [
            {
                "title": job.titulo,
                "company": job.empresa,
                "match_score": analysis.match_score,
            }
            for analysis, job in top_jobs
        ],
        "top_missing_skills": top_missing_skills,
    }