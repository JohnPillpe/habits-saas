from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.models import Usuario
from sqlalchemy.orm import Session

from app.services.interview_service import (
    start_interview,
    answer_interview,
)

router = APIRouter(
    prefix="/api/interview",
    tags=["Interview"],
)


@router.post("/start")
def start(
    role: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return start_interview(
        db=db,
        user_id=usuario.id,
        role=role,
    )


@router.post("/answer")
def answer(
    session_id: int,
    answer: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return answer_interview(
        db=db,
        session_id=session_id,
        answer=answer,
    )