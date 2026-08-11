import re


def normalize_text(value: str) -> str:
    """
    Normaliza un texto para comparar variantes como:

    Full-Stack
    Full Stack
    fullstack
    """

    value = str(value or "").lower()

    # Sustituir separadores por espacios
    value = re.sub(r"[-_/]", " ", value)

    # Eliminar caracteres especiales
    value = re.sub(r"[^a-z0-9+#. ]", " ", value)

    # Normalizar espacios
    value = re.sub(r"\s+", " ", value).strip()

    return value


def compact_text(value: str) -> str:
    """
    Elimina espacios para poder comparar:

    full stack
    full-stack
    fullstack
    """

    return normalize_text(value).replace(" ", "")


def is_relevant_job(
    job: dict,
    keywords: list[str],
) -> bool:

    tags = job.get("tags", [])

    if isinstance(tags, list):
        tags_text = " ".join(
            str(tag) for tag in tags
        )
    else:
        tags_text = str(tags or "")

    text = " ".join([
        str(job.get("title", "")),
        str(job.get("category", "")),
        tags_text,
        str(job.get("description", "")),
        str(job.get("company", "")),
    ])

    normalized_text = normalize_text(text)
    compact_job_text = compact_text(text)

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        compact_keyword = compact_text(
            keyword
        )

        if not normalized_keyword:
            continue

        # Coincidencia normal
        if normalized_keyword in normalized_text:
            return True

        # Coincidencia ignorando espacios/separadores
        if compact_keyword in compact_job_text:
            return True

    return False