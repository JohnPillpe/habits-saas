from app.models.models import InterviewSession


def create_interview(db, user_id, role):

    session = InterviewSession(
        user_id=user_id,
        role=role,
        current_question=0,
        score=0,
        answers=[],
        finished=False,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_interview(db, session_id):

    return (
        db.query(InterviewSession)
        .filter(InterviewSession.id == session_id)
        .first()
    )

def save_answer(db, session, answer):

    answers = session.answers or []
    answers.append(answer)

    session.answers = answers
    session.current_question += 1

    db.commit()
    db.refresh(session)

    return session


def finish_interview(db, session, score):

    session.finished = True
    session.score = score

    db.commit()
    db.refresh(session)

    return session