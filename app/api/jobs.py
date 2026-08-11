from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import JobOffer

from app.core.auth import get_current_user
from app.models.models import Usuario
from app.services.job_search_service import search_jobs_for_user


router = APIRouter(
    prefix="/job-offers",
    tags=["Jobs"],
)


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

    jobs = query.order_by(
        JobOffer.published_at.desc()
    ).all()

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
            "match_score": job.match_score,
        }
        for job in jobs
    ]

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
        "match_score": job.match_score,
    }

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