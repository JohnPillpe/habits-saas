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
    ]).lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )