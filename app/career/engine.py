import json

from app.career.cv_service import obtener_cv
from app.career.analyzer import analizar_oferta
from app.models.models import JobOffer
from app.services.career_analysis_service import guardar_analisis
from app.career.cv_optimizer import optimizar_cv
from app.services.optimized_cv_service import guardar_cv_optimizado



def analizar_ofertas_usuario(usuario_id: int, db):

    cv = obtener_cv(usuario_id)

    if not cv:
        return []

    ofertas = (
        db.query(JobOffer)
        .filter(JobOffer.usuario_id == usuario_id)
        .all()
    )

    print(len(ofertas))

    resultados = []

    for oferta in ofertas:

        job = f"""
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

        analisis = analizar_oferta(
            cv=cv,
            job=job,
        )

        cv_optimizado = optimizar_cv(
            cv=cv,
            job=job,
        )

        print("CV OPTIMIZADO GENERADO")
        print(cv_optimizado[:300])

        guardar_cv_optimizado(
            db=db,
            job_offer_id=oferta.id,
            content=cv_optimizado,
        )

        print("CV GUARDADO:", oferta.id)
        
        guardar_analisis(
            db=db,
            job_offer_id=oferta.id,
            analisis=analisis,
        )

        print(oferta.titulo)
        print(json.dumps(analisis, indent=2))
        print("----------------")

        resultados.append({
            "oferta": oferta,
            "analisis": analisis,
        })

        resultados.sort(
            key=lambda x: x["analisis"]["match_score"],
            reverse=True,
        )

    return resultados