from app.services.interview_questions import QUESTIONS
from app.services.interview_session_service import (
    create_interview,
    get_interview,
    save_answer,
    finish_interview,
)
from app.services.interview_evaluator import evaluate_interview


def _select_questions(role: str):

    role = role.lower()

    if "backend" in role or "python" in role:
        return QUESTIONS["backend"]

    if "frontend" in role:
        return QUESTIONS["frontend"]

    if "marketing" in role:
        return QUESTIONS["marketing"]

    return QUESTIONS["backend"]


def start_interview(
    db,
    user_id,
    role: str,
):

    questions = _select_questions(role)

    session = create_interview(
        db=db,
        user_id=user_id,
        role=role,
    )

    return {
        "finished": False,
        "session_id": session.id,
        "question": questions[0],
        "question_number": 1,
        "total_questions": len(questions),
    }


def answer_interview(
    db,
    session_id: int,
    answer: str,
):

    session = get_interview(
        db,
        session_id,
    )

    if not session:
        return {
            "error": "Interview not found."
        }

    questions = _select_questions(
        session.role,
    )

    session = save_answer(
        db,
        session,
        answer,
    )

    if session.current_question >= len(questions):

        evaluation = evaluate_interview(
            role=session.role,
            questions=questions,
            answers=session.answers,
        )

        finish_interview(
            db=db,
            session=session,
            score=100,
        )

        return {
            "finished": True,
            "evaluation": evaluation,
        }

    return {
        "finished": False,
        "question": questions[
            session.current_question
        ],
        "question_number": session.current_question + 1,
        "total_questions": len(questions),
    }