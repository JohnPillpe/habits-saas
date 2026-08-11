import re

from app.rag.vector_store import obtener_documento_completo
from app.services.job_offer_service import obtener_oferta


# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def _normalize_text(value):
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
    text = _normalize_text(value).lower()

    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text.replace(" ", "")


# --------------------------------------------------
# KEYWORDS
# --------------------------------------------------

def _extract_keywords(text):
    text = _normalize_text(text).lower()

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}",
        text,
    )

    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "you",
        "your",
        "our",
        "are",
        "this",
        "that",
        "from",
        "have",
        "will",
        "they",
        "their",
        "about",
        "into",
        "over",
        "work",
        "working",
        "years",
        "year",
        "experience",
        "team",
        "role",
        "job",
    }

    return {
        word
        for word in words
        if word not in stopwords
        and len(word) > 2
    }


# --------------------------------------------------
# JOB TEXT
# --------------------------------------------------

def _build_job_text(job):
    title = _normalize_text(
        job.get("title")
        or job.get("titulo")
    )

    description = _normalize_text(
        job.get("description")
        or job.get("descripcion")
    )

    category = _normalize_text(
        job.get("category")
        or job.get("categoria")
    )

    tags = _normalize_text(
        job.get("tags")
    )

    return " ".join([
        title,
        category,
        tags,
        description,
    ])


# --------------------------------------------------
# CV ↔ JOB MATCH
# --------------------------------------------------

def calculate_cv_job_match(
    cv_text: str,
    job: dict,
):
    """
    Calculates how well the user's CV matches
    a specific job.

    This score is independent from the search query.
    """

    if not cv_text:
        return {
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    job_text = _build_job_text(job)

    if not job_text:
        return {
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    cv_keywords = _extract_keywords(cv_text)
    job_keywords = _extract_keywords(job_text)

    if not job_keywords:
        return {
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    compact_cv = _compact_text(cv_text)

    matched = []
    missing = []

    for keyword in job_keywords:

        if (
            keyword in cv_keywords
            or keyword in compact_cv
        ):
            matched.append(keyword)
        else:
            missing.append(keyword)

    keyword_ratio = (
        len(matched) / len(job_keywords)
    )

    # --------------------------------------------------
    # TITLE SIGNAL
    # --------------------------------------------------

    title = _normalize_text(
        job.get("title")
        or job.get("titulo")
    ).lower()

    title_words = _extract_keywords(title)

    title_matches = sum(
        1
        for word in title_words
        if word in cv_keywords
        or word in compact_cv
    )

    if title_words:
        title_ratio = (
            title_matches / len(title_words)
        )
    else:
        title_ratio = 0

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    score = (
        keyword_ratio * 80
        + title_ratio * 20
    )

    score = round(
        max(0, min(score, 100))
    )

    return {
        "match_score": score,
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
    }


# --------------------------------------------------
# PUBLIC FUNCTION
# --------------------------------------------------

def calculate_user_job_match(
    db,
    user_id: int,
    job_offer_id: int,
):
    """
    Loads the user's CV and a specific job,
    then calculates CV ↔ Job compatibility.
    """

    # --------------------------------------------------
    # 1. GET JOB
    # --------------------------------------------------

    job = obtener_oferta(
        db=db,
        job_offer_id=job_offer_id,
    )

    if not job:
        return None

    # --------------------------------------------------
    # 2. GET CV
    # --------------------------------------------------

    cv_text = obtener_documento_completo(
        usuario_id=user_id,
        nombre_documento=None,
    )

    if not cv_text:
        return {
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    # --------------------------------------------------
    # 3. CALCULATE
    # --------------------------------------------------

    resultado = calculate_cv_job_match(
        cv_text=cv_text,
        job=job,
    )

    return resultado