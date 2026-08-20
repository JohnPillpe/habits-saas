from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import JobOffer

from app.core.auth import get_current_user
from app.models.models import Usuario
from app.services.job_search_service import search_jobs_for_user

from app.services.location_service import (
    REGIONS,
    COUNTRIES,
    normalize_country,
    get_countries_for_region,
    get_cities,
)


router = APIRouter(
    prefix="/job-offers",
    tags=["Jobs"],
)


# ============================================================
# PUBLIC JOB SEARCH
# ============================================================

@router.get("/public")
def listar_ofertas_publicas(
    keyword: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    published: Optional[str] = None,
    workType: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(JobOffer)

    # --------------------------------------------------
    # Ignore incomplete / pasted placeholder jobs
    # --------------------------------------------------

    query = query.filter(
        JobOffer.enlace.isnot(None),
        JobOffer.enlace != "",
        JobOffer.titulo.isnot(None),
        JobOffer.titulo != "Pasted Job",
    )

    # --------------------------------------------------
    # KEYWORD
    # --------------------------------------------------

    if keyword:
        search = keyword.strip().lower()

        query = query.filter(
            JobOffer.titulo.ilike(f"%{search}%")
            | JobOffer.empresa.ilike(f"%{search}%")
            | JobOffer.categoria.ilike(f"%{search}%")
            | JobOffer.descripcion.ilike(f"%{search}%")
        )

    # --------------------------------------------------
    # COUNTRY
    # --------------------------------------------------

    if country:
        query = query.filter(
            JobOffer.country.ilike(
                f"%{country.strip()}%"
            )
        )

    # --------------------------------------------------
    # CITY
    # --------------------------------------------------

    if city:
        query = query.filter(
            JobOffer.city.ilike(
                f"%{city.strip()}%"
            )
        )

    # --------------------------------------------------
    # WORK TYPE
    # --------------------------------------------------

    if workType:
        query = query.filter(
            JobOffer.work_type.ilike(
                f"%{workType.strip()}%"
            )
        )

    # --------------------------------------------------
    # PUBLISHED
    # --------------------------------------------------

    if published:
        try:
            days = int(published)

            date_limit = (
                datetime.utcnow()
                - timedelta(days=days)
            )

            query = query.filter(
                JobOffer.published_at >= date_limit
            )

        except ValueError:
            pass

    # --------------------------------------------------
    # EXECUTE
    # --------------------------------------------------

    jobs = (
        query
        .order_by(JobOffer.published_at.desc())
        .all()
    )

    return [
        {
            "id": job.id,
            "title": job.titulo,
            "company": job.empresa,
            "url": job.enlace,
            "category": job.categoria,
            "salary": job.salario,
            "description": job.descripcion,
            "tags": (
                job.tags.split(", ")
                if job.tags
                else []
            ),
            "country": job.country,
            "city": job.city,
            "work_type": job.work_type,
            "published_at": (
                job.published_at.isoformat()
                if job.published_at
                else None
            ),
            "logo": job.logo,
            "source": job.source,

            # IMPORTANT:
            # Public users NEVER receive personalized Match Score.
            "match_score": None,
        }
        for job in jobs
    ]


# ============================================================
# LOCATIONS
# ============================================================

@router.get("/locations")
def get_job_locations(
    db: Session = Depends(get_db),
):
    rows = (
        db.query(
            JobOffer.country,
            JobOffer.city,
        )
        .filter(
            JobOffer.country.isnot(None),
            JobOffer.city.isnot(None),
        )
        .distinct()
        .order_by(
            JobOffer.country.asc(),
            JobOffer.city.asc(),
        )
        .all()
    )

    return [
        {
            "country": country,
            "city": city,
        }
        for country, city in rows
        if country and city
    ]


@router.get("/locations/countries")
def search_countries(
    q: str | None = None,
    region: str | None = None,
):
    query = (q or "").strip().lower()
    selected_region = (region or "").strip()

    if selected_region:
        countries = get_countries_for_region(
            selected_region
        )
    else:
        countries = list(COUNTRIES)

    if query:
        exact_matches = []
        prefix_matches = []
        contains_matches = []

        for country in countries:
            country_lower = country.lower()

            if country_lower == query:
                exact_matches.append(country)

            elif country_lower.startswith(query):
                prefix_matches.append(country)

            elif query in country_lower:
                contains_matches.append(country)

        countries = (
            exact_matches
            + prefix_matches
            + contains_matches
        )

    else:
        countries = sorted(
            countries,
            key=str.lower,
        )

    if selected_region:
        regions = [selected_region]
    else:
        regions = sorted(
            [
                region_name
                for region_name in REGIONS
                if (
                    not query
                    or query in region_name.lower()
                )
            ],
            key=str.lower,
        )

    return {
        "regions": regions,
        "countries": countries[:50],
    }


@router.get("/locations/cities")
def search_cities(
    q: str | None = None,
    country: str | None = None,
    db: Session = Depends(get_db),
):
    city_query = (q or "").strip()
    selected_country = normalize_country(country)

    catalog_cities = get_cities(
        country=selected_country,
        query=city_query,
    )

    db_query = (
        db.query(JobOffer.city)
        .filter(
            JobOffer.city.isnot(None),
            JobOffer.city != "",
        )
    )

    if selected_country:
        db_query = db_query.filter(
            JobOffer.country.ilike(
                selected_country
            )
        )

    if city_query:
        db_query = db_query.filter(
            JobOffer.city.ilike(
                f"%{city_query}%"
            )
        )

    database_cities = [
        city
        for (city,) in (
            db_query
            .distinct()
            .order_by(JobOffer.city.asc())
            .limit(100)
            .all()
        )
        if city
    ]

    cities = sorted(
        set(
            catalog_cities
            + database_cities
        ),
        key=str.lower,
    )

    return cities[:50]


# ============================================================
# PUBLIC JOB DETAIL
# ============================================================

@router.get("/public/{job_id}")
def obtener_oferta_publica(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = (
        db.query(JobOffer)
        .filter(JobOffer.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "id": job.id,
        "title": job.titulo,
        "company": job.empresa,
        "url": job.enlace,
        "category": job.categoria,
        "salary": job.salario,
        "description": job.descripcion,
        "tags": (
            job.tags.split(", ")
            if job.tags
            else []
        ),
        "country": job.country,
        "city": job.city,
        "work_type": job.work_type,
        "published_at": (
            job.published_at.isoformat()
            if job.published_at
            else None
        ),
        "logo": job.logo,
        "source": job.source,

        # --------------------------------------------------
        # PUBLIC DETAIL
        # --------------------------------------------------
        # Never expose Match Score to unauthenticated users.
        "match_score": None,
    }


# ============================================================
# AUTHENTICATED SEARCH
# ============================================================

@router.get("/search")
def buscar_ofertas_usuario(
    keyword: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    published: Optional[str] = None,
    workType: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    resultado = search_jobs_for_user(
        db=db,
        user_id=usuario.id,
        search=keyword,
        country=country,
        city=city,
        published=published,
        work_type=workType,
    )

    return resultado["jobs"]


# ============================================================
# DEBUG
# ============================================================

@router.get("/debug/locations")
def debug_locations(
    db: Session = Depends(get_db),
):
    jobs = (
        db.query(
            JobOffer.country,
            JobOffer.city,
        )
        .distinct()
        .all()
    )

    return [
        {
            "country": country,
            "city": city,
        }
        for country, city in jobs
    ]