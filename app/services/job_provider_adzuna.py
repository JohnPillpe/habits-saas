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

ADZUNA_COUNTRY_CODE = "gb"
ADZUNA_CURRENCY = "£"


def buscar_ofertas_adzuna(
    palabra: str,
    max_ofertas: int = 20,
):
    """
    Busca ofertas en Adzuna y las convierte
    al formato estándar del sistema.

    Adzuna es solamente un provider.

    No contiene:
    - lógica de búsqueda global
    - scoring
    - relevancia
    - matching
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

    url = (
        f"{ADZUNA_BASE_URL}/"
        f"{ADZUNA_COUNTRY_CODE}/search/1"
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
                "error": (
                    "Error connecting to Adzuna: "
                    f"{str(e)}"
                )
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

        if not isinstance(job, dict):
            continue

        # --------------------------------------------------
        # BASIC DATA
        # --------------------------------------------------

        title = (
            job.get("title")
            or "Unknown"
        )

        company_data = (
            job.get("company")
            or {}
        )

        company = (
            company_data.get(
                "display_name"
            )
            or "Unknown"
        )

        url = (
            job.get("redirect_url")
            or ""
        ).strip()

        # --------------------------------------------------
        # LOCATION
        # --------------------------------------------------

        country, city = _build_location(
            job
        )

        # --------------------------------------------------
        # TAGS / SKILLS
        # --------------------------------------------------

        tags = _build_tags(
            job.get("skills")
        )

        # --------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------

        # IMPORTANT:
        # We intentionally use only the description
        # supplied by the Adzuna API.
        #
        # We do NOT scrape the Adzuna website because
        # Adzuna can return HTTP 403/404 for detail pages.

        description = (
            job.get("description")
            or ""
        ).strip()

        # --------------------------------------------------
        # NORMALIZE
        # --------------------------------------------------

        resultados.append(
            normalize_job_offer(

                source="Adzuna",

                title=title,

                company=company,

                url=url,

                category=(
                    (
                        job.get(
                            "category"
                        )
                        or {}
                    ).get(
                        "label"
                    )
                ),

                salary=_build_salary(
                    job
                ),

                description=description,

                tags=tags,

                country=country,

                city=city,

                work_type=_build_work_type(
                    job
                ),

                published_at=job.get(
                    "created"
                ),

                logo=None,
            )
        )

    return resultados


def _build_location(job):
    """
    Convierte la localización de Adzuna
    al formato estándar del sistema.
    """

    location = (
        job.get("location")
        or {}
    )

    area = (
        location.get("area")
        or []
    )

    country = None
    city = None

    if isinstance(area, list):

        cleaned_area = [
            str(value).strip()
            for value in area
            if value
        ]

        if cleaned_area:
            country = (
                cleaned_area[0]
            )

        if len(cleaned_area) >= 2:
            city = (
                cleaned_area[-1]
            )

    display_name = (
        location.get(
            "display_name"
        )
    )

    if not city and display_name:

        city = (
            str(display_name)
            .split(",")[0]
            .strip()
        )

    return country, city


def _build_tags(skills):
    """
    Normaliza skills de Adzuna.
    """

    if not skills:
        return []

    if isinstance(skills, list):

        return [
            str(skill).strip()
            for skill in skills
            if skill is not None
        ]

    return [
        str(skills).strip()
    ]


def _build_work_type(job):
    """
    Normaliza el tipo de contrato.
    """

    contract_time = (
        job.get("contract_time")
        or ""
    ).strip().lower()

    contract_type = (
        job.get("contract_type")
        or ""
    ).strip().lower()

    if contract_time:
        return _normalize_work_type(
            contract_time
        )

    if contract_type:
        return _normalize_work_type(
            contract_type
        )

    return None


def _normalize_work_type(value):
    """
    Normaliza valores conocidos de Adzuna.
    """

    mapping = {
        "full_time": "full_time",
        "part_time": "part_time",
        "contract": "contract",
        "permanent": "permanent",
        "temporary": "temporary",
    }

    return mapping.get(
        value,
        value,
    )


def _build_salary(job):
    """
    Construye el salario normalizado.

    Adzuna UK puede no proporcionar
    salary_currency, por lo que usamos GBP.
    """

    minimum = job.get(
        "salary_min"
    )

    maximum = job.get(
        "salary_max"
    )

    if (
        minimum is None
        and maximum is None
    ):
        return None

    currency = (
        job.get(
            "salary_currency"
        )
        or ADZUNA_CURRENCY
    )

    minimum_text = (
        _format_salary_number(
            minimum
        )
        if minimum is not None
        else None
    )

    maximum_text = (
        _format_salary_number(
            maximum
        )
        if maximum is not None
        else None
    )

    if (
        minimum_text is not None
        and maximum_text is not None
    ):

        return (
            f"{currency}"
            f"{minimum_text} - "
            f"{currency}"
            f"{maximum_text}"
        )

    if minimum_text is not None:

        return (
            f"{currency}"
            f"{minimum_text}+"
        )

    return (
        "Up to "
        f"{currency}"
        f"{maximum_text}"
    )


def _format_salary_number(value):
    """
    Ejemplo:

    28498.42 -> 28,498
    70000    -> 70,000
    """

    try:
        return f"{float(value):,.0f}"

    except (
        TypeError,
        ValueError,
    ):
        return str(value)