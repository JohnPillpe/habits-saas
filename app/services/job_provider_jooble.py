import requests

from app.core.config import JOOBLE_API_KEY

from app.services.job_normalizer_service import (
    normalize_job_offer,
)


JOOBLE_BASE_URL = "https://es.jooble.org/api"


def buscar_ofertas_jooble(
    palabra: str,
    max_ofertas: int = 10,
    location: str = "",
):
    """
    Busca ofertas en Jooble y las convierte
    al formato estándar del sistema.

    Jooble es solamente un provider.
    No contiene lógica de búsqueda global,
    relevancia ni scoring.
    """

    if not JOOBLE_API_KEY:
        return [
            {
                "error": (
                    "Jooble API key is not configured"
                )
            }
        ]

    url = (
        f"{JOOBLE_BASE_URL}/"
        f"{JOOBLE_API_KEY}"
    )

    payload = {
        "keywords": palabra,
        "location": location,
        "page": "1",
        "ResultOnPage": max_ofertas,
        "companysearch": "false",
    }

    headers = {
        "Content-Type": "application/json",
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:

        print(
            "[JOOBLE] Request error:",
            str(e),
        )

        return [
            {
                "error": (
                    f"Jooble request error: {str(e)}"
                )
            }
        ]

    except ValueError as e:

        print(
            "[JOOBLE] Invalid JSON:",
            str(e),
        )

        return [
            {
                "error": (
                    "Jooble returned invalid JSON"
                )
            }
        ]

    jobs = data.get(
        "jobs",
        [],
    )

    resultados = []

    for job in jobs[:max_ofertas]:

        if not isinstance(job, dict):
            continue

        title = (
            job.get("title")
            or "Unknown"
        )

        company = (
            job.get("company")
            or "Unknown"
        )

        description = (
            job.get("snippet")
            or ""
        )

        url = (
            job.get("link")
            or ""
        )

        if not url:
            continue

        location_value = (
            job.get("location")
            or ""
        )

        city = None
        country = None

        if location_value:

            location_parts = [
                part.strip()
                for part in str(
                    location_value
                ).split(",")
                if part.strip()
            ]

            if location_parts:
                city = location_parts[0]

            if len(location_parts) >= 2:
                country = location_parts[-1]

        resultados.append(
            normalize_job_offer(
                source="Jooble",
                title=title,
                company=company,
                url=url,
                category=None,
                salary=(
                    job.get("salary")
                    or None
                ),
                description=description,
                tags=[],
                country=country,
                city=city,
                work_type=(
                    job.get("type")
                    or None
                ),
                published_at=(
                    job.get("updated")
                    or None
                ),
                logo=None,
            )
        )

    print(
        f"[JOOBLE] {len(resultados)} jobs "
        f"found for '{palabra}'"
    )

    return resultados