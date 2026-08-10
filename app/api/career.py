from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.models import Usuario

from app.models.models import CareerAnalysis

from app.career.schemas_api import CareerRequest

from app.career.cv_service import obtener_cv
from app.services.job_offer_service import obtener_oferta
from app.models.models import OptimizedCV
from app.models.models import CoverLetter
from app.models.models import ApplicationAnswers
from app.models.models import InterviewPreparation
from app.services.dashboard_service import obtener_dashboard
from app.services.job_search_service import search_jobs_for_user


from app.schemas.schemas import (
    UserJobPreferenceCreate,
    UserJobPreferenceResponse,
)

from app.services.user_job_preference_service import (
    get_user_job_preference,
    save_user_job_preference,
)

from app.career.engine import analizar_oferta_usuario

router = APIRouter(
    prefix="/api/career",
    tags=["career"],
)

@router.post("/analyze")
def analyze(
    request: CareerRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):

    resultado = analizar_oferta_usuario(
        usuario_id=usuario.id,
        job_offer_id=request.job_offer_id,
        db=db,
    )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Could not analyze job",
        )

    analisis = resultado["analisis"]

    return {
        "match_score": analisis["match_score"],
        "recommendation": analisis["recommendation"],
        "summary": analisis["summary"],
        "why": analisis["why"],
        "strengths": analisis["strengths"],
        "missing_skills": analisis["missing_skills"],
        "required_skills": analisis["required_skills"],
        "soft_skills": analisis["soft_skills"],
        "seniority": analisis["seniority"],
        "difficulty": analisis["difficulty"],
        "next_steps": analisis["next_steps"],
    }

@router.get("/optimized-cv/{job_offer_id}")
def obtener_cv_optimizado(
    job_offer_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    cv = (
        db.query(OptimizedCV)
        .filter(
            OptimizedCV.job_offer_id == job_offer_id
        )
        .first()
    )

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="Optimized CV not found",
        )

    return {
        "job_offer_id": cv.job_offer_id,
        "content": cv.content,
    }


@router.get("/cover-letter/{job_offer_id}")
def obtener_cover_letter(
    job_offer_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    cover = (
        db.query(CoverLetter)
        .filter(
            CoverLetter.job_offer_id == job_offer_id
        )
        .first()
    )

    if not cover:
        raise HTTPException(
            status_code=404,
            detail="Cover Letter not found",
        )

    return {
        "job_offer_id": cover.job_offer_id,
        "content": cover.content,
    }


@router.get("/application-answers/{job_offer_id}")
def obtener_application_answers(
    job_offer_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    answers = (
        db.query(ApplicationAnswers)
        .filter(
            ApplicationAnswers.job_offer_id == job_offer_id
        )
        .first()
    )

    if not answers:
        raise HTTPException(
            status_code=404,
            detail="Application Answers not found",
        )

    return {
        "tell_me_about_yourself": answers.tell_me_about_yourself,
        "why_this_company": answers.why_this_company,
        "why_should_we_hire_you": answers.why_should_we_hire_you,
        "greatest_strength": answers.greatest_strength,
        "greatest_weakness": answers.greatest_weakness,
    }


@router.get("/interview-preparation/{job_offer_id}")
def obtener_interview_preparation(
    job_offer_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    prep = (
        db.query(InterviewPreparation)
        .filter(
            InterviewPreparation.job_offer_id == job_offer_id
        )
        .first()
    )

    if not prep:
        raise HTTPException(
            status_code=404,
            detail="Interview preparation not found",
        )

    return {
        "technical_questions": prep.technical_questions,
        "behavioral_questions": prep.behavioral_questions,
        "tips": prep.tips,
    }

@router.post("/preferences", response_model=UserJobPreferenceResponse)
def save_preferences(
    data: UserJobPreferenceCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return save_user_job_preference(
        db=db,
        user_id=usuario.id,
        data=data,
    )