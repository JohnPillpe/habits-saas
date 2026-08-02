from app.services.habit_service import (
    get_habits_context,
)

from app.services.user_job_preference_service import (
    get_job_preference_context,
)


def build_user_context(
    db,
    user_id: int,
):
    """
    Construye el contexto que recibirá el agente.
    """

    partes = []

    # Preferencias laborales
    job_context = get_job_preference_context(
        db,
        user_id,
    )

    if job_context:
        partes.append(job_context)

    # Hábitos
    habits_context = get_habits_context(
        db,
        user_id,
    )

    if habits_context:
        partes.append(habits_context)

    return "\n\n".join(partes)