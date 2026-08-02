import requests

from app.services.job_normalizer_service import normalize_job_offer


def buscar_ofertas_swissdevjobs(
    palabra: str,
    max_ofertas: int = 20,
):
    url = "https://swissdevjobs.ch/api/jobs/"

    try:
        response = requests.get(
            url,
            timeout=10,
        )
        response.raise_for_status()

        jobs = response.json()

        palabra = palabra.lower()

        resultados = []

        for job in jobs:

            texto = (
                job.get("title", "")
                + " "
                + job.get("company", "")
                + " "
                + job.get("technologies", "")
            ).lower()

            if palabra not in texto:
                continue

            resultados.append(
                normalize_job_offer(
                    source="SwissDevJobs",

                    title=job.get("title", "Unknown"),

                    company=job.get("company", "Unknown"),

                    url=job.get("url", ""),

                    category="Software",

                    salary=job.get("salary"),

                    tags=job.get("technologies"),

                    work_type=None,

                    country=job.get("country"),

                    city=job.get("city"),

                    published_at=job.get("published_at"),

                    logo=None,
                )
            )

            if len(resultados) >= max_ofertas:
                break

        return resultados

    except requests.RequestException as e:
        return [{"error": str(e)}]