from app.services.location_service import (
    extract_country,
)


def normalize_existing_job_locations(db):
    from app.models.models import JobOffer

    jobs = (
        db.query(JobOffer)
        .all()
    )

    updated = 0

    for job in jobs:

        normalized_country = extract_country(
            job.country
        )

        if normalized_country != job.country:

            job.country = normalized_country
            updated += 1

    db.commit()

    return updated