import re


def _normalize_text(value):
    """
    Convierte strings, listas y otros valores
    en texto comparable.
    """

    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(
            str(item)
            for item in value
            if item is not None
        )

    return str(value)


def _compact_text(value):
    """
    Normaliza eliminando espacios y separadores.

    Ejemplos:
    Full Stack
    Full-Stack
    FullStack

    -> fullstack
    """

    text = _normalize_text(value).lower()

    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text.replace(" ", "")


def _get_job_field(job, *names):
    """
    Permite trabajar tanto con los nombres
    actuales como con nombres antiguos.
    """

    for name in names:
        value = job.get(name)

        if value is not None and value != "":
            return value

    return ""


def _keyword_matches(keyword, job_text, compact_job_text):
    """
    Comprueba si una keyword aparece en el job.
    """

    normalized_keyword = _normalize_text(
        keyword
    ).lower().strip()

    if not normalized_keyword:
        return False

    normalized_keyword = re.sub(
        r"\s+",
        " ",
        normalized_keyword,
    )

    if normalized_keyword in job_text:
        return True

    compact_keyword = _compact_text(
        keyword
    )

    if (
        compact_keyword
        and compact_keyword in compact_job_text
    ):
        return True

    return False


def calculate_match_score(
    job,
    skill_gap=None,
    preference=None,
    search=None,
):
    """
    Calculates a fast deterministic match score.

    This is NOT the deep AI career analysis.

    The score is based on:

    - Desired role / keywords
    - Job title
    - Category
    - Tags
    - Description
    - Country
    - City
    - Work type

    Maximum score: 100
    """

    # --------------------------------------------------
    # JOB DATA
    # --------------------------------------------------

    title = _normalize_text(
        _get_job_field(
            job,
            "title",
            "titulo",
        )
    ).lower()

    category = _normalize_text(
        _get_job_field(
            job,
            "category",
            "categoria",
        )
    ).lower()

    tags = _normalize_text(
        job.get("tags", "")
    ).lower()

    description = _normalize_text(
        _get_job_field(
            job,
            "description",
            "descripcion",
        )
    ).lower()

    company = _normalize_text(
        _get_job_field(
            job,
            "company",
            "empresa",
        )
    ).lower()

    job_text = " ".join([
        title,
        category,
        tags,
        description,
        company,
    ])

    compact_job_text = _compact_text(
        job_text
    )

    score = 0

        # --------------------------------------------------
    # SEARCH QUERY MATCH
    # --------------------------------------------------

    if search and str(search).strip():

        search_text = _normalize_text(
            search
        ).lower().strip()

        search_words = [
            word
            for word in search_text.split()
            if len(word) > 2
        ]

        if search_words:

            matched_search_words = sum(
                1
                for word in search_words
                if _keyword_matches(
                    word,
                    job_text,
                    compact_job_text,
                )
            )

            search_ratio = (
                matched_search_words
                / len(search_words)
            )

            # Search relevance = maximum 50 points
            score += round(
                search_ratio * 50
            )


    # --------------------------------------------------
    # USER PREFERENCES
    # --------------------------------------------------

    if preference:

        # ----------------------------------------------
        # 1. DESIRED ROLE
        # ----------------------------------------------

        desired_role = _normalize_text(
            getattr(
                preference,
                "desired_role",
                "",
            )
        ).lower().strip()

        if desired_role:

            role_words = [
                word
                for word in desired_role.split()
                if len(word) > 2
            ]

            if role_words:

                matched_words = sum(
                    1
                    for word in role_words
                    if _keyword_matches(
                        word,
                        job_text,
                        compact_job_text,
                    )
                )

                role_ratio = (
                    matched_words / len(role_words)
                )

                # Desired role = maximum 50 points
                score += round(
                    role_ratio * 50
                )

        # ----------------------------------------------
        # 2. COUNTRY
        # ----------------------------------------------

        target_countries = getattr(
            preference,
            "target_countries",
            [],
        ) or []

        job_country = _normalize_text(
            job.get("country", "")
        ).lower()

        if target_countries and job_country:

            country_match = any(
                _normalize_text(country).lower()
                in job_country
                for country in target_countries
                if _normalize_text(country).strip()
            )

            if country_match:
                score += 15

        # ----------------------------------------------
        # 3. CITY
        # ----------------------------------------------

        target_cities = getattr(
            preference,
            "target_cities",
            [],
        ) or []

        job_city = _normalize_text(
            job.get("city", "")
        ).lower()

        if target_cities and job_city:

            city_match = any(
                _normalize_text(city).lower()
                in job_city
                for city in target_cities
                if _normalize_text(city).strip()
            )

            if city_match:
                score += 10

        # ----------------------------------------------
        # 4. WORK TYPE
        # ----------------------------------------------

        job_work_type = _normalize_text(
            job.get("work_type", "")
        ).lower()

        if job_work_type:

            if (
                getattr(
                    preference,
                    "remote",
                    False,
                )
                and "remote" in job_work_type
            ):
                score += 15

            elif (
                getattr(
                    preference,
                    "hybrid",
                    False,
                )
                and "hybrid" in job_work_type
            ):
                score += 15

            elif (
                getattr(
                    preference,
                    "onsite",
                    False,
                )
                and (
                    "onsite" in job_work_type
                    or "on-site" in job_work_type
                )
            ):
                score += 15

    # --------------------------------------------------
    # 5. JOB QUALITY / TITLE SIGNAL
    # --------------------------------------------------

    if title:
        score += 5

    # --------------------------------------------------
    # LIMIT
    # --------------------------------------------------

    return min(
        max(score, 0),
        100,
    )