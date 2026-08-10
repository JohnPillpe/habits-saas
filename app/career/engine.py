from app.career.cv_service import obtener_cv
from app.career.analyzer import analizar_oferta
from app.models.models import JobOffer

from app.services.career_analysis_service import guardar_analisis

from app.career.cv_optimizer import optimizar_cv
from app.services.optimized_cv_service import guardar_cv_optimizado

from app.career.cover_letter_generator import generar_cover_letter
from app.services.cover_letter_service import guardar_cover_letter

from app.career.application_answers import generar_respuestas
from app.services.application_answers_service import guardar_application_answers

from app.career.interview_preparation import generar_preparacion_entrevista
from app.services.interview_preparation_service import guardar_interview_preparation


def construir_job(oferta):

    if oferta.descripcion:
        return oferta.descripcion

    return f"""
Título:
{oferta.titulo}

Empresa:
{oferta.empresa}

Categoría:
{oferta.categoria}

Tags:
{oferta.tags}

Salario:
{oferta.salario}
"""


def analizar_oferta_usuario(
    usuario_id: int,
    job_offer_id: int,
    db,
):
    # -----------------------------------
    # 1. CV
    # -----------------------------------

    print("DEBUG usuario_id:", usuario_id)
    print("DEBUG job_offer_id:", job_offer_id)

    cv = obtener_cv(usuario_id)

    print("DEBUG CV:", cv is not None)

    # -----------------------------------
    # 2. JOB SELECCIONADO
    # -----------------------------------

    oferta = (
        db.query(JobOffer)
        .filter(
            JobOffer.id == job_offer_id,
        )
        .first()
    )

    print("DEBUG OFERTA:", oferta is not None)

    if not cv:
        print("DEBUG ERROR: NO CV")
        return None

    if not oferta:
        print("DEBUG ERROR: JOB NOT FOUND")
        return None

    job = construir_job(oferta)

    print("\n====================================")
    print("ANALIZANDO JOB:", oferta.id)
    print(oferta.titulo)
    print("====================================\n")

    # -----------------------------------
    # 3. AI ANALYSIS
    # -----------------------------------

    analisis = analizar_oferta(
        cv=cv,
        job=job,
    )

    guardar_analisis(
        db=db,
        job_offer_id=oferta.id,
        analisis=analisis,
    )

    print("ANALYSIS GUARDADA:", oferta.id)
    print("MATCH:", analisis.get("match_score"))

    # -----------------------------------
    # 4. OPTIMIZED CV
    # -----------------------------------

    cv_optimizado = optimizar_cv(
        cv=cv,
        job=job,
    )

    guardar_cv_optimizado(
        db=db,
        job_offer_id=oferta.id,
        content=cv_optimizado,
    )

    print("CV GUARDADO:", oferta.id)

    # -----------------------------------
    # 5. COVER LETTER
    # -----------------------------------

    cover_letter = generar_cover_letter(
        cv=cv,
        job=job,
    )

    guardar_cover_letter(
        db=db,
        job_offer_id=oferta.id,
        content=cover_letter,
    )

    print("COVER LETTER GUARDADA:", oferta.id)

    # -----------------------------------
    # 6. APPLICATION ANSWERS
    # -----------------------------------

    application_answers = generar_respuestas(
        cv=cv,
        job=job,
    )

    guardar_application_answers(
        db=db,
        job_offer_id=oferta.id,
        respuestas_json=application_answers,
    )

    print(
        "APPLICATION ANSWERS GUARDADAS:",
        oferta.id,
    )

    # -----------------------------------
    # 7. INTERVIEW PREPARATION
    # -----------------------------------

    interview_preparation = (
        generar_preparacion_entrevista(
            cv=cv,
            job=job,
        )
    )

    guardar_interview_preparation(
        db=db,
        job_offer_id=oferta.id,
        preparation_json=interview_preparation,
    )

    print(
        "INTERVIEW PREPARATION GUARDADA:",
        oferta.id,
    )

    # -----------------------------------
    # 8. RESULT
    # -----------------------------------

    return {
        "oferta": oferta,
        "analisis": analisis,
    }