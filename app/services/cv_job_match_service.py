import re

from app.rag.vector_store import obtener_documento_completo
from app.services.job_offer_service import obtener_oferta


# ============================================================
# TEXT UTILITIES
# ============================================================

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
        "company",
        "looking",
        "using",
        "used",
        "strong",
        "ability",
        "including",
        "responsibilities",
        "required",
        "requirements",
    }

    return {
        word
        for word in words
        if word not in stopwords
        and len(word) > 2
    }


# ============================================================
# JOB TEXT
# ============================================================

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

    return {
        "title": title,
        "description": description,
        "category": category,
        "tags": tags,
    }


# ============================================================
# GENERIC KEYWORD MATCH
# ============================================================

def _keyword_match_score(
    cv_text,
    target_text,
):
    target_keywords = _extract_keywords(
        target_text
    )

    if not target_keywords:
        return 0, [], []

    cv_keywords = _extract_keywords(
        cv_text
    )

    compact_cv = _compact_text(
        cv_text
    )

    matched = []
    missing = []

    for keyword in target_keywords:

        if (
            keyword in cv_keywords
            or keyword in compact_cv
        ):
            matched.append(keyword)

        else:
            missing.append(keyword)

    score = (
        len(matched)
        / len(target_keywords)
        * 100
    )

    return (
        round(score),
        sorted(matched),
        sorted(missing),
    )


# ============================================================
# SENIORITY SIGNAL
# ============================================================

def _seniority_score(
    cv_text,
    job_text,
):
    cv_lower = _normalize_text(
        cv_text
    ).lower()

    job_lower = _normalize_text(
        job_text
    ).lower()

    senior_keywords = {
        "senior",
        "lead",
        "head",
        "director",
        "manager",
        "principal",
        "chief",
    }

    cv_senior = any(
        word in cv_lower
        for word in senior_keywords
    )

    job_senior = any(
        word in job_lower
        for word in senior_keywords
    )

    if job_senior and cv_senior:
        return 100

    if not job_senior:
        return 100

    return 30


# ============================================================
# MAIN MATCH ENGINE
# ============================================================

def calculate_cv_job_match(
    cv_text: str,
    job: dict,
):
    """
    Deterministic weighted CV ↔ Job matching engine.

    Returns a transparent score between 0 and 100.
    """

    if not cv_text:
        return {
            "match_score": 0,
            "skills_score": 0,
            "title_score": 0,
            "responsibilities_score": 0,
            "industry_score": 0,
            "seniority_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    sections = _build_job_text(
        job
    )

    # --------------------------------------------------------
    # 1. SKILLS
    # --------------------------------------------------------

    skills_score, skills_matched, skills_missing = (
        _keyword_match_score(
            cv_text,
            sections["tags"],
        )
    )

    # --------------------------------------------------------
    # 2. TITLE
    # --------------------------------------------------------

    title_score, title_matched, title_missing = (
        _keyword_match_score(
            cv_text,
            sections["title"],
        )
    )

    # --------------------------------------------------------
    # 3. RESPONSIBILITIES
    # --------------------------------------------------------

    responsibilities_score, resp_matched, resp_missing = (
        _keyword_match_score(
            cv_text,
            sections["description"],
        )
    )

    # --------------------------------------------------------
    # 4. INDUSTRY / CATEGORY
    # --------------------------------------------------------

    industry_score, industry_matched, industry_missing = (
        _keyword_match_score(
            cv_text,
            sections["category"],
        )
    )

    # --------------------------------------------------------
    # 5. SENIORITY
    # --------------------------------------------------------

    seniority_score = _seniority_score(
        cv_text,
        sections["title"] + " "
        + sections["description"],
    )

    # --------------------------------------------------------
    # 6. WEIGHTED SCORE
    # --------------------------------------------------------

    final_score = (
        skills_score * 0.40
        + title_score * 0.20
        + responsibilities_score * 0.20
        + industry_score * 0.10
        + seniority_score * 0.10
    )

    final_score = round(
        max(
            0,
            min(
                final_score,
                100,
            ),
        )
    )

    matched_keywords = sorted(
        set(
            skills_matched
            + title_matched
            + resp_matched
            + industry_matched
        )
    )

    missing_keywords = sorted(
        set(
            skills_missing
            + title_missing
            + resp_missing
            + industry_missing
        )
    )

    return {
        "match_score": final_score,

        "skills_score": skills_score,

        "title_score": title_score,

        "responsibilities_score": (
            responsibilities_score
        ),

        "industry_score": industry_score,

        "seniority_score": seniority_score,

        "matched_keywords": (
            matched_keywords
        ),

        "missing_keywords": (
            missing_keywords
        ),
    }


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def calculate_user_job_match(
    db,
    user_id: int,
    job_offer_id: int,
):
    """
    Loads the user's CV and a specific job,
    then calculates CV ↔ Job compatibility.
    """

    job = obtener_oferta(
        db=db,
        oferta_id=job_offer_id,
        usuario_id=user_id,
    )

    if not job:
        return None

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

    job_dict = {
        "title": job.titulo,
        "description": job.descripcion,
        "category": job.categoria,
        "tags": job.tags,
    }

    return calculate_cv_job_match(
        cv_text=cv_text,
        job=job_dict,
    )