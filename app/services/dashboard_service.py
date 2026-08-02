from collections import Counter
from sqlalchemy.orm import Session
from app.services.career_insights_service import generate_career_insights

from app.models.models import (
    CareerAnalysis,
    JobOffer,
    InterviewSession,
    UserJobPreference,
)


def obtener_dashboard(
    db: Session,
    user_id: int,
):

    analisis = (
        db.query(CareerAnalysis)
        .join(JobOffer)
        .filter(JobOffer.usuario_id == user_id)
        .all()
    )

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
        .join(JobOffer)
        .filter(JobOffer.usuario_id == user_id)
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

    interviews = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == user_id)
        .all()
    )

    completed_interviews = sum(
        1 for interview in interviews if interview.finished
    )

    average_interview_score = (
        round(
            sum(i.score for i in interviews) / len(interviews)
        )
        if interviews
        else 0
    )


    career_score = round(
        promedio * 0.7
        + average_interview_score * 0.3
    )

    next_action = None

    if top_missing_skills:
        next_action = (
            f"Learn {top_missing_skills[0]['skill']}. "
            "It appears frequently in your analyzed jobs."
    )

    next_action = None

    if top_missing_skills:
        skill = top_missing_skills[0]["skill"]

        next_action = (
            f"Your next priority should be learning {skill}. "
            f"It appears in {top_missing_skills[0]['count']} analyzed job offers."
        )

    insights = generate_career_insights(
        career_score=career_score,
        average_match=round(promedio),
        interview_score=average_interview_score,
        habits=0,
        missing_skills=[
            s["skill"] for s in top_missing_skills
        ],
    )



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
        "interviews_completed": completed_interviews,
        "career_score": career_score,
        "next_action": next_action,
        "career_insights": insights,

    }