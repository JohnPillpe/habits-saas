from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.models.models import JobOffer, Usuario
from app.core.auth import get_current_user

from app.career.service import analizar_cv_vs_job
from app.services.rag_service import get_cv_text
from app.services.career_analysis_service import guardar_analisis

from app.services.job_url_service import extract_job_from_url


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


# ==========================================
# ANALYZE EXISTING JOB
# ==========================================

@router.post("/job/{job_id}")
def analyze_job(
    job_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
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

    

    job_text = f"""
Title:
{job.titulo}

Company:
{job.empresa}

Category:
{job.categoria}

Tags:
{job.tags}

Salary:
{job.salario}
"""



# ==========================================
# ANALYZE JOB URL
# ==========================================

class JobURLRequest(BaseModel):
    url: str


@router.post("/url")
def analyze_job_url(
    data: JobURLRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    try:
        job_data = extract_job_from_url(data.url)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not extract job: {str(e)}",
        )

    job = JobOffer(
        titulo=job_data["title"],
        empresa=job_data["company"],
        categoria=None,
        salario=None,
        tags=None,
        enlace=job_data["url"],
        usuario_id=usuario.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "title": job.titulo,
        "company": job.empresa,
        "url": job.enlace,
    }


# ==========================================
# ANALYZE PASTED JOB — NEW
# ==========================================

class JobPasteRequest(BaseModel):
    content: str


@router.post("/paste")
def analyze_pasted_job(
    data: JobPasteRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    if not data.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Job posting cannot be empty",
        )

    # Create a job offer from the pasted job
    job = JobOffer(
        titulo="Pasted Job",
        empresa="Unknown",
        categoria=None,
        salario=None,
        tags=None,
        enlace="pasted-job",
        descripcion=data.content,
        usuario_id=usuario.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "title": job.titulo,
        "company": job.empresa,
        "url": job.enlace,
    }