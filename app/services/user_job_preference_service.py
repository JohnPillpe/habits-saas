from sqlalchemy.orm import Session

from app.models.models import UserJobPreference


def get_user_job_preference(db: Session, user_id: int):
    return (
        db.query(UserJobPreference)
        .filter(UserJobPreference.user_id == user_id)
        .first()
    )


def save_user_job_preference(
    db: Session,
    user_id: int,
    data,
):
    preference = get_user_job_preference(db, user_id)

    if preference:
        preference.desired_role = data.desired_role
        preference.target_countries = data.target_countries
        preference.target_cities = data.target_cities
        preference.remote = data.remote
        preference.hybrid = data.hybrid
        preference.onsite = data.onsite
        preference.published_within_days = data.published_within_days
    else:
        preference = UserJobPreference(
            user_id=user_id,
            desired_role=data.desired_role,
            target_countries=data.target_countries,
            target_cities=data.target_cities,
            remote=data.remote,
            hybrid=data.hybrid,
            onsite=data.onsite,
            published_within_days=data.published_within_days,
        )

        db.add(preference)

    db.commit()
    db.refresh(preference)

    return preference

def get_job_preference_context(
    db,
    user_id: int,
):
    """
    Devuelve las preferencias laborales del usuario como contexto.
    """

    preference = get_user_job_preference(
        db,
        user_id,
    )

    if not preference:
        return ""

    modalidades = []

    if preference.remote:
        modalidades.append("Remote")

    if preference.hybrid:
        modalidades.append("Hybrid")

    if preference.onsite:
        modalidades.append("On-site")

    countries = ", ".join(preference.target_countries) if preference.target_countries else "Sin preferencia"

    cities = ", ".join(preference.target_cities) if preference.target_cities else "Sin preferencia"

    return f"""
Objetivo profesional: {preference.desired_role}

Países objetivo: {countries}

Ciudades objetivo: {cities}

Modalidad: {", ".join(modalidades)}

Buscar ofertas publicadas en los últimos {preference.published_within_days} días.
""".strip()