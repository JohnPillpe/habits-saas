from sqlalchemy.orm import Session

from app.services.job_provider_remotive import (
    buscar_ofertas_remotive,
)
from app.services.job_provider_swissdevjobs import (
    buscar_ofertas_swissdevjobs,
)
from app.services.user_job_preference_service import (
    get_user_job_preference,
)

from app.services.career_coach_service import (
    build_career_advice,
)

from app.intelligence.market_analyzer import analyze_market
from app.services.market_report_service import build_market_report
from app.services.skill_gap_service import analyze_skill_gap
from app.services.rag_service import get_cv_text
from app.services.job_keyword_service import build_search_keywords
from app.services.job_relevance_service import is_relevant_job
from app.services.job_match_service import calculate_match_score

JOB_PROVIDERS = [
    buscar_ofertas_remotive,
    buscar_ofertas_swissdevjobs,
]

def search_jobs_for_user(
    db: Session,
    user_id: int,
    search: str | None = None,
):
    preference = get_user_job_preference(
        db,
        user_id,
    )

    if search:
        keywords = build_search_keywords(search)

    elif preference:
        keywords = build_search_keywords(preference.desired_role)

    else:
        return []

    jobs = []
    seen_links = set()

    for keyword in keywords:

        for provider in JOB_PROVIDERS:

            provider_jobs = provider(
                palabra=keyword,
                max_ofertas=10,
            )

            if not provider_jobs:
                continue

            if "error" in provider_jobs[0]:
                continue

            for job in provider_jobs:

                link = job.get("url", "").strip()

                if link in seen_links:
                    continue

                if not is_relevant_job(job, keywords):
                    continue

                seen_links.add(link)
                jobs.append(job)

    analysis = analyze_market(jobs)

    market_report = build_market_report(analysis)

    cv_text = get_cv_text(user_id)

    skill_gap = analyze_skill_gap(
        cv_text=cv_text,
        market_analysis=analysis,
    )

    career_advice = build_career_advice(
        skill_gap,
        market_report,
        preference,
    )

    for job in jobs:

        job["match_score"] = calculate_match_score(
            job,
            skill_gap,
            preference,
        )

    jobs.sort(
        key=lambda x: x["match_score"],
        reverse=True,
    )



    return {
        "jobs": jobs,
        "analysis": analysis,
        "market_report": market_report,
        "skill_gap": skill_gap,
        "career_advice": career_advice,
    }