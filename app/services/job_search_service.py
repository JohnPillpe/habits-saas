from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.models import JobOffer

from app.services.job_provider_remotive import (
    buscar_ofertas_remotive,
)

from app.services.user_job_preference_service import (
    get_user_job_preference,
)

from app.services.job_keyword_service import (
    build_search_keywords,
)

from app.services.job_relevance_service import (
    is_relevant_job,
)

from app.services.job_match_service import (
    calculate_match_score,
)

from app.services.cv_job_match_service import (
    calculate_cv_job_match,
)

from app.career.cv_service import (
    obtener_cv,
)

from app.services.job_provider_adzuna import (
    buscar_ofertas_adzuna,
)


JOB_PROVIDERS = [
    buscar_ofertas_remotive,
    buscar_ofertas_adzuna,
]


def _tags_to_string(tags):
    if isinstance(tags, list):
        return ", ".join(
            str(tag)
            for tag in tags
            if tag is not None
        )

    return tags

def _normalize_text(value) -> str:
    if not value:
        return ""

    return " ".join(
        str(value)
        .strip()
        .lower()
        .split()
    )


def _build_job_dedup_key(job: dict) -> str:
    company = _normalize_text(
        job.get("company")
    )

    title = _normalize_text(
        job.get("title")
    )

    description = _normalize_text(
        job.get("description")
    )

    # Usamos las primeras palabras de la descripción
    # para identificar anuncios prácticamente idénticos.
    description_fingerprint = " ".join(
        description.split()[:40]
    )

    return (
        f"{company}|"
        f"{title}|"
        f"{description_fingerprint}"
    )




def _save_job(
    db: Session,
    job: dict,
    user_id: int,
):
    url = (job.get("url") or "").strip()

    if not url:
        return None

    existing_job = (
        db.query(JobOffer)
        .filter(JobOffer.enlace == url)
        .first()
    )

    if existing_job:
        db_job = existing_job

    else:
        db_job = JobOffer(
            enlace=url,
            usuario_id=user_id,
        )

        db.add(db_job)

    db_job.titulo = (
        job.get("title")
        or "Unknown"
    )

    db_job.empresa = (
        job.get("company")
        or "Unknown"
    )

    db_job.descripcion = job.get(
        "description"
    )

    db_job.categoria = job.get(
        "category"
    )

    db_job.salario = job.get(
        "salary"
    )

    db_job.tags = _tags_to_string(
        job.get("tags")
    )

    db_job.country = job.get(
        "country"
    )

    db_job.city = job.get(
        "city"
    )

    db_job.work_type = job.get(
        "work_type"
    )

    db_job.published_at = job.get(
    "published_at"
    )

    db_job.source = job.get(
        "source"
    )

    db_job.logo = job.get(
        "logo"
    )

    db.flush()

    return db_job


def search_jobs_for_user(
    db: Session,
    user_id: int,
    search: str | None = None,
    country: str | None = None,
    city: str | None = None,
    published: str | None = None,
    work_type: str | None = None,
):
    """
    Main job-search pipeline.
    """

    preference = get_user_job_preference(
        db,
        user_id,
    )

    # --------------------------------------------------
    # 1. BUILD SEARCH KEYWORDS
    # --------------------------------------------------

    if search and search.strip():

        keywords = build_search_keywords(
            search.strip()
        )

    elif preference:

        keywords = build_search_keywords(
            preference.desired_role
        )

    else:

        return {
            "jobs": [],
        }

    # --------------------------------------------------
    # 2. SEARCH PROVIDERS
    # --------------------------------------------------

    jobs = []
    seen_links = set()
    seen_job_keys = set()

    for keyword in keywords:

        for provider in JOB_PROVIDERS:

            try:

                provider_jobs = provider(
                    palabra=keyword,
                    max_ofertas=10,
                )

            except Exception:

                continue

            if not provider_jobs:
                continue

            if (
                isinstance(provider_jobs[0], dict)
                and "error" in provider_jobs[0]
            ):
                continue

            for job in provider_jobs:

                if not isinstance(job, dict):
                    continue

                link = (
                    job.get("url")
                    or ""
                ).strip()

                if not link:
                    continue

                if link in seen_links:
                    continue
                
                dedup_key = _build_job_dedup_key(
                    job
                )

                if dedup_key in seen_job_keys:
                    continue

                # ------------------------------------------
                # RELEVANCE
                # ------------------------------------------

                if not is_relevant_job(
                    job,
                    keywords,
                ):
                    continue

                seen_links.add(link)

                seen_job_keys.add(
                    dedup_key
                )

                jobs.append(job)

    # --------------------------------------------------
    # 3. COUNTRY FILTER
    # --------------------------------------------------

    if country and country.strip():

        country_search = (
            country.strip().lower()
        )

        jobs = [
            job
            for job in jobs
            if country_search in str(
                job.get("country", "")
            ).lower()
        ]

    # --------------------------------------------------
    # 4. CITY FILTER
    # --------------------------------------------------

    if city and city.strip():

        city_search = (
            city.strip().lower()
        )

        jobs = [
            job
            for job in jobs
            if city_search in str(
                job.get("city", "")
            ).lower()
        ]

    # --------------------------------------------------
    # 5. WORK TYPE FILTER
    # --------------------------------------------------

    if work_type and work_type.strip():

        work_type_search = (
            work_type.strip().lower()
        )

        jobs = [
            job
            for job in jobs
            if work_type_search in str(
                job.get("work_type", "")
            ).lower()
        ]

    # --------------------------------------------------
    # 6. PUBLISHED FILTER
    # --------------------------------------------------

    if published and published.strip():

        try:

            days = int(
                published.strip()
            )

            date_limit = (
                datetime.utcnow()
                - timedelta(days=days)
            )

            filtered_jobs = []

            for job in jobs:

                published_at = job.get(
                    "published_at"
                )

                if not published_at:
                    continue

                try:

                    published_date = (
                        datetime.fromisoformat(
                            str(
                                published_at
                            ).replace(
                                "Z",
                                "+00:00",
                            )
                        )
                    )

                    # Para comparar de forma segura
                    published_date = (
                        published_date.replace(
                            tzinfo=None
                        )
                    )

                    if published_date >= date_limit:
                        filtered_jobs.append(job)

                except (ValueError, TypeError):

                    continue

            jobs = filtered_jobs

        except ValueError:

            pass

    # --------------------------------------------------
    # 7. SAVE / UPDATE DATABASE
    # --------------------------------------------------

    for job in jobs:

        db_job = _save_job(
            db=db,
            job=job,
            user_id=user_id,
        )

        if db_job:

            job["id"] = db_job.id

    db.commit()

    # --------------------------------------------------
    # 8. MATCH SCORE
    # --------------------------------------------------

    cv_text = obtener_cv(user_id)

    for job in jobs:

        # ----------------------------------------------
        # WITH CV → CV ↔ JOB MATCH
        # ----------------------------------------------

        if cv_text:

            match_result = calculate_cv_job_match(
                cv_text=cv_text,
                job=job,
            )

            job["match_score"] = (
                match_result["match_score"]
            )

        # ----------------------------------------------
        # WITHOUT CV → FAST SEARCH MATCH
        # ----------------------------------------------

        else:

            job["match_score"] = (
                calculate_match_score(
                    job=job,
                    skill_gap=None,
                    preference=preference,
                    search=search,
                )
            )

        # ----------------------------------------------
        # SAVE SCORE
        # ----------------------------------------------

        db_job = (
            db.query(JobOffer)
            .filter(
                JobOffer.id == job["id"]
            )
            .first()
        )

        if db_job:

            db_job.match_score = (
                job["match_score"]
            )

    db.commit()



    # --------------------------------------------------
    # 9. SORT
    # --------------------------------------------------

    jobs.sort(
        key=lambda job: (
            job.get("match_score") or 0
        ),
        reverse=True,
    )

    # --------------------------------------------------
    # 10. RESPONSE
    # --------------------------------------------------

    return {
        "jobs": jobs,
    }