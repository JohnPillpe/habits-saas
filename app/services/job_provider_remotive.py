import requests

from app.services.job_normalizer_service import (
    normalize_job_offer,
)


def extract_country(value: str | None) -> str | None:
    """
    Intenta extraer un país desde el campo
    candidate_required_location de Remotive.

    Remotive puede devolver valores como:

    France
    United Kingdom
    Europe, EMEA, UK, Germany, France
    Worldwide
    Northern America, Europe, UK, France

    Por ahora conservamos el valor completo cuando
    no podemos identificar un país de forma segura.
    """

    if not value:
        return None

    value = str(value).strip()

    if not value:
        return None

    return value


def buscar_ofertas_remotive(
    palabra: str,
    max_ofertas: int = 5,
) -> list[dict[str, object]]:
    """
    Busca ofertas de empleo en Remotive usando su API pública.

    Remotive es solamente un provider.
    No contiene lógica de búsqueda global,
    relevancia ni scoring.
    """

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": palabra,
        "limit": max_ofertas,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:
        return [
            {
                "error": (
                    "Error conectando con Remotive: "
                    f"{str(e)}"
                )
            }
        ]

    except ValueError as e:
        return [
            {
                "error": (
                    "Remotive returned invalid JSON: "
                    f"{str(e)}"
                )
            }
        ]

    jobs = data.get(
        "jobs",
        [],
    )

    palabra_lower = (
        palabra.strip().lower()
    )

    jobs_filtrados = []

    for job in jobs:

        title = (
            job.get("title")
            or ""
        )

        tags = (
            job.get("tags")
            or []
        )

        if isinstance(tags, list):

            tags_text = " ".join(
                str(tag)
                for tag in tags
                if tag is not None
            )

        else:

            tags_text = str(tags)

        searchable_text = (
            f"{title} {tags_text}"
        ).lower()

        if (
            not palabra_lower
            or palabra_lower in searchable_text
        ):

            jobs_filtrados.append(
                job
            )

    ofertas = []

    for job in jobs_filtrados[:max_ofertas]:

        candidate_location = (
            job.get(
                "candidate_required_location"
            )
        )

        ofertas.append(
            normalize_job_offer(

                source="Remotive",

                title=(
                    job.get("title")
                    or "Unknown"
                ),

                company=(
                    job.get("company_name")
                    or "Unknown"
                ),

                url=(
                    job.get("url")
                    or ""
                ),

                category=job.get(
                    "category"
                ),

                salary=job.get(
                    "salary"
                ),

                description=job.get(
                    "description"
                ),

                tags=job.get(
                    "tags",
                    [],
                ),

                work_type="Remote",

                country=extract_country(
                    candidate_location
                ),

                city=None,

                published_at=job.get(
                    "publication_date"
                ),

                logo=job.get(
                    "company_logo"
                ),
            )
        )

    return ofertas