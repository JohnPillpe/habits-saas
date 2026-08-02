def is_relevant_job(job: dict, keywords: list[str]) -> bool:
    """
    Devuelve True si la oferta contiene alguna palabra clave.
    """

    text = " ".join([
        job.get("titulo", ""),
        job.get("categoria", ""),
        job.get("tags", ""),
    ]).lower()

    for keyword in keywords:
        if keyword.lower() in text:
            return True

    return False