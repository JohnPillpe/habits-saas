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
    Permite trabajar tanto con nombres
    actuales como antiguos.
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

    normalized_keyword = (
        _normalize_text(keyword)
        .lower()
        .strip()
    )

    if not normalized_keyword:
        return False

    normalized_keyword = re.sub(
        r"\s+",
        " ",
        normalized_keyword,
    )

    if normalized_keyword in job_text:
        return True

    compact_keyword = _compact_text(keyword)

    if (
        compact_keyword
        and compact_keyword in compact_job_text
    ):
        return True

    return False


def _keyword_match_score(
    keyword,
    title,
    category,
    tags,
    description,
):
    """
    Calcula la relevancia de una keyword.

    Title     = fuerte
    Category  = medio
    Tags      = medio
    Desc      = débil
    """

    keyword = _normalize_text(keyword).lower().strip()

    if not keyword:
        return 0

    compact_keyword = _compact_text(keyword)

    title_compact = _compact_text(title)
    category_compact = _compact_text(category)
    tags_compact = _compact_text(tags)
    description_compact = _compact_text(description)

    # ----------------------------------------------
    # EXACT / COMPACT MATCH
    # ----------------------------------------------

    if compact_keyword and compact_keyword in title_compact:
        return 40

    if compact_keyword and compact_keyword in category_compact:
        return 25

    if compact_keyword and compact_keyword in tags_compact:
        return 20

    if compact_keyword and compact_keyword in description_compact:
        return 5

    return 0


def calculate_match_score(
    job,
    skill_gap=None,
    preference=None,
    search=None,
):
    """
    Fast deterministic Match Score.

    Maximum: 100

    Prioridades:

    1. Search query
    2. Desired role
    3. Country
    4. City
    5. Work type
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

    score = 0

    # ==================================================
    # 1. SEARCH QUERY
    # ==================================================

    if search and str(search).strip():

        search_words = [
            word
            for word in _normalize_text(search)
            .lower()
            .split()
            if len(word) > 2
        ]

        if search_words:

            search_score = 0

            for word in search_words:

                search_score += _keyword_match_score(
                    keyword=word,
                    title=title,
                    category=category,
                    tags=tags,
                    description=description,
                )

            # Maximum search contribution = 60
            search_score = min(
                search_score,
                60,
            )

            score += search_score

    # ==================================================
    # 2. USER PREFERENCES
    # ==================================================

    if preference:

        # ----------------------------------------------
        # DESIRED ROLE
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
                        " ".join([
                            title,
                            category,
                            tags,
                            description,
                        ]),
                        _compact_text(
                            " ".join([
                                title,
                                category,
                                tags,
                                description,
                            ])
                        ),
                    )
                )

                role_ratio = (
                    matched_words
                    / len(role_words)
                )

                # Maximum = 20
                score += round(
                    role_ratio * 20
                )

        # ----------------------------------------------
        # COUNTRY
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
                _normalize_text(country)
                .lower()
                .strip()
                in job_country
                for country in target_countries
                if _normalize_text(country).strip()
            )

            if country_match:
                score += 10

        # ----------------------------------------------
        # CITY
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
                _normalize_text(city)
                .lower()
                .strip()
                in job_city
                for city in target_cities
                if _normalize_text(city).strip()
            )

            if city_match:
                score += 5

        # ----------------------------------------------
        # WORK TYPE
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
                score += 5

            elif (
                getattr(
                    preference,
                    "hybrid",
                    False,
                )
                and "hybrid" in job_work_type
            ):
                score += 5

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
                score += 5

    # ==================================================
    # 3. VALID JOB SIGNAL
    # ==================================================

    if title:
        score += 5

    # ==================================================
    # LIMIT
    # ==================================================

    return min(
        max(score, 0),
        100,
    )