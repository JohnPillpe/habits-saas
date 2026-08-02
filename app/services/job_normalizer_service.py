from typing import Any


def normalize_job_offer(
    *,
    source: str,
    title: str,
    company: str,
    url: str,
    category: str | None = None,
    salary: str | None = None,
    tags: str | list[str] | None = None,
    country: str | None = None,
    city: str | None = None,
    work_type: str | None = None,
    published_at: str | None = None,
    logo: str | None = None,
) -> dict[str, Any]:

    return {
        "title": title,
        "company": company,
        "url": url,

        "category": category,
        "salary": salary,
        "tags": tags,

        "country": country,
        "city": city,

        "work_type": work_type,

        "published_at": published_at,

        "logo": logo,

        "source": source,
    }