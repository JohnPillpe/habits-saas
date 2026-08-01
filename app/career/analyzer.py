from app.career.service import analizar_cv_vs_job


def analizar_oferta(
    cv: str,
    job: str,
):
    return analizar_cv_vs_job(
        cv=cv,
        job=job,
    )