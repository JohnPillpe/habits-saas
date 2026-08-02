import requests
from typing import List, Dict
from app.services.job_normalizer_service import normalize_job_offer


def buscar_ofertas_remotive(
    palabra: str,
    max_ofertas: int = 5,
) -> list[dict[str, object]]:
    """
    Busca ofertas de empleo en Remotive usando su API pública.
    """

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": palabra,
        "limit": max_ofertas
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
       
        response.raise_for_status()

        data = response.json()

        jobs = data.get("jobs", [])

        palabra_lower = palabra.lower()

        jobs_filtrados = [
            job for job in jobs
            if palabra_lower in (
                job.get("title", "") +
                " " +
                " ".join(job.get("tags", []))
            ).lower()
        ]

        ofertas = []

        for job in jobs_filtrados[:max_ofertas]:

            ofertas.append(
                normalize_job_offer(
                    source="Remotive",

                    title=job.get("title", "Unknown"),

                    company=job.get("company_name", "Unknown"),

                    url=job.get("url", ""),

                    category=job.get("category"),

                    salary=job.get("salary"),

                    tags=job.get("tags", []),

                    work_type="Remote",

                    country=None,

                    city=None,

                    published_at=job.get("publication_date"),

                    logo=job.get("company_logo"),
                )
            )

        return ofertas


    except requests.RequestException as e:

        return [
            {
                "error": f"Error conectando con Remotive: {str(e)}"
            }
        ]       


