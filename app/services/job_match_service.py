def _normalize_text(value):
    """
    Convierte strings, listas y otros valores
    en un texto comparable.
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


def _get_job_field(job, *names):
    """
    Permite trabajar tanto con los nombres
    actuales de Remotive como con nombres antiguos.
    """

    for name in names:
        value = job.get(name)

        if value is not None and value != "":
            return value

    return ""


def calculate_match_score(
    job,
    skill_gap=None,
    preference=None,
):
    """
    Calcula un score de compatibilidad entre
    el usuario y una oferta.

    El score combina:
    - título
    - categoría
    - tags
    - descripción
    - role deseado
    - tipo de trabajo
    - país
    - ciudad
    """

    # --------------------------------------------------
    # JOB DATA
    # --------------------------------------------------

    titulo = _normalize_text(
        _get_job_field(
            job,
            "title",
            "titulo",
        )
    ).lower()

    categoria = _normalize_text(
        _get_job_field(
            job,
            "category",
            "categoria",
        )
    ).lower()

    tags = _normalize_text(
        job.get("tags", "")
    ).lower()

    descripcion = _normalize_text(
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

    texto_job = " ".join([
        titulo,
        categoria,
        tags,
        descripcion,
        company,
    ])

    score = 0

    # --------------------------------------------------
    # PREFERENCE
    # --------------------------------------------------

    if preference:

        desired_role = _normalize_text(
            getattr(
                preference,
                "desired_role",
                "",
            )
        ).lower()

        preferred_work_type = _normalize_text(
            getattr(
                preference,
                "work_type",
                "",
            )
        ).lower()

        preferred_country = _normalize_text(
            getattr(
                preference,
                "country",
                "",
            )
        ).lower()

        preferred_city = _normalize_text(
            getattr(
                preference,
                "city",
                "",
            )
        ).lower()

        # ----------------------------------------------
        # DESIRED ROLE
        # ----------------------------------------------

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
                    if word in texto_job
                )

                role_ratio = (
                    matched_words / len(role_words)
                )

                score += round(
                    role_ratio * 40
                )

        # ----------------------------------------------
        # WORK TYPE
        # ----------------------------------------------

        if preferred_work_type:

            job_work_type = _normalize_text(
                job.get(
                    "work_type",
                    "",
                )
            ).lower()

            if preferred_work_type in job_work_type:
                score += 15

        # ----------------------------------------------
        # COUNTRY
        # ----------------------------------------------

        if preferred_country:

            job_country = _normalize_text(
                job.get(
                    "country",
                    "",
                )
            ).lower()

            if preferred_country in job_country:
                score += 10

        # ----------------------------------------------
        # CITY
        # ----------------------------------------------

        if preferred_city:

            job_city = _normalize_text(
                job.get(
                    "city",
                    "",
                )
            ).lower()

            if preferred_city in job_city:
                score += 5

    # --------------------------------------------------
    # SEARCH / ROLE RELEVANCE
    # --------------------------------------------------

    # Si existe título, damos una pequeña base
    # porque tenemos una oferta válida.
    if titulo:
        score += 5

    # --------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------

    # IMPORTANTE:
    #
    # missing_skills NO se premian.
    #
    # Son skills que le faltan al usuario.
    #
    # De momento dejamos esta sección preparada
    # para que posteriormente podamos comparar
    # las skills reales del CV contra las skills
    # requeridas por cada job.

    # --------------------------------------------------
    # LIMIT
    # --------------------------------------------------

    return min(
        max(score, 0),
        100,
    )