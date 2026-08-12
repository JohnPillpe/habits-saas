from app.core.config import (
    ADZUNA_APP_ID,
    ADZUNA_APP_KEY,
)

import requests

from app.services.job_normalizer_service import (
    normalize_job_offer,
)


ADZUNA_BASE_URL = (
    "https://api.adzuna.com/v1/api/jobs"
)


def buscar_ofertas_adzuna(
    palabra: str,
    max_ofertas: int = 20,
):
    """
    Busca ofertas en Adzuna y las convierte
    al formato estándar del sistema.

    Adzuna es solamente un provider.
    No contiene lógica de búsqueda global,
    relevancia ni scoring.
    """

    app_id = ADZUNA_APP_ID
    app_key = ADZUNA_APP_KEY

    if not app_id or not app_key:
        return [
            {
                "error": (
                    "Adzuna API credentials "
                    "are not configured"
                )
            }
        ]

    country_code = "gb"

    url = (
        f"{ADZUNA_BASE_URL}/"
        f"{country_code}/search/1"
    )

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": palabra,
        "results_per_page": max_ofertas,
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
                "error": str(e)
            }
        ]

    except ValueError as e:
        return [
            {
                "error": (
                    "Adzuna returned invalid JSON: "
                    f"{e}"
                )
            }
        ]

    results = data.get(
        "results",
        [],
    )

    resultados = []

    for job in results:

        # DEBUG:
        # Mostramos temporalmente la respuesta
        # original de Adzuna para comprobar
        # exactamente qué campos devuelve.
        print(
            "\n========== ADZUNA RAW JOB =========="
        )
        print(job)
        print(
            "====================================\n"
        )

        location = job.get(
            "location"
        ) or {}

        area = location.get(
            "area"
        ) or []

        country = None
        city = None

        if isinstance(area, list):

            if area:
                city = area[-1]

            if len(area) >= 2:
                country = area[0]

        tags = job.get(
            "skills"
        ) or []

        resultados.append(
            normalize_job_offer(

                source="Adzuna",

                title=job.get(
                    "title",
                    "Unknown",
                ),

                company=(
                    (job.get("company") or {})
                    .get("display_name")
                    or "Unknown"
                ),

                url=job.get(
                    "redirect_url",
                    "",
                ),

                category=(
                    job.get("category", {})
                    or {}
                ).get(
                    "label"
                ),

                salary=_build_salary(
                    job
                ),

                description=job.get(
                    "description"
                ),

                tags=tags,

                country=country,

                city=city,

                work_type=job.get("contract_time"),

                published_at=job.get(
                    "created"
                ),

                logo=None,
            )
        )

    return resultados


def _build_salary(job):

    minimum = job.get(
        "salary_min"
    )

    maximum = job.get(
        "salary_max"
    )

    if minimum is None and maximum is None:
        return None

    currency = job.get(
        "salary_currency"
    )

    if minimum is not None and maximum is not None:
        return (
            f"{currency or ''}"
            f"{minimum:,.0f} - "
            f"{maximum:,.0f}"
        ).strip()

    if minimum is not None:
        return (
            f"{currency or ''}"
            f"{minimum:,.0f}+"
        ).strip()

    return (
        f"Up to "
        f"{currency or ''}"
        f"{maximum:,.0f}"
    ).strip()