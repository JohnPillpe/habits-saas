import requests
from bs4 import BeautifulSoup


def extract_job_from_url(url: str) -> dict:
    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = None
    company = None

    # Title
    if soup.find("meta", property="og:title"):
        title = soup.find(
            "meta",
            property="og:title"
        ).get("content")

    if not title and soup.title:
        title = soup.title.get_text(strip=True)

    # Description
    description = ""

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description:
        description = meta_description.get("content", "")

    # Basic fallback
    if not title:
        raise ValueError("Could not extract job title")

    return {
        "title": title,
        "company": company or "Unknown",
        "description": description,
        "url": url,
    }