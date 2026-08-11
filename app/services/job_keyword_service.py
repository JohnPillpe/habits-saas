def build_search_keywords(role: str) -> list[str]:
    """
    Convierte un rol introducido por el usuario
    en varias búsquedas útiles.

    Genera variantes genéricas para que los providers
    puedan encontrar el mismo concepto aunque utilicen
    espacios, guiones o palabras unidas.
    """

    role = (role or "").strip().lower()

    if not role:
        return []

    keywords = []

    # --------------------------------------------------
    # ORIGINAL ROLE
    # --------------------------------------------------

    keywords.append(role)

    # --------------------------------------------------
    # GENERIC ROLE VARIANTS
    # --------------------------------------------------

    # "full stack" -> "full-stack" / "fullstack"
    if " " in role:
        keywords.append(
            role.replace(" ", "-")
        )

        keywords.append(
            role.replace(" ", "")
        )

    # "full-stack" -> "full stack" / "fullstack"
    if "-" in role:
        keywords.append(
            role.replace("-", " ")
        )

        keywords.append(
            role.replace("-", "")
        )

    # --------------------------------------------------
    # PYTHON
    # --------------------------------------------------

    if "python" in role:
        keywords.extend([
            "Python",
            "FastAPI",
            "Django",
            "Backend Engineer",
        ])

    # --------------------------------------------------
    # AI / MACHINE LEARNING
    # --------------------------------------------------

    if (
        "ai" in role
        or "artificial intelligence" in role
        or "machine learning" in role
        or "ml engineer" in role
    ):
        keywords.extend([
            "AI Engineer",
            "Machine Learning Engineer",
            "ML Engineer",
            "AI Architect",
        ])

    # --------------------------------------------------
    # DATA
    # --------------------------------------------------

    if (
        "data" in role
        or "data engineer" in role
        or "data science" in role
    ):
        keywords.extend([
            "Data Engineer",
            "Data Scientist",
            "Data Science",
        ])

    # --------------------------------------------------
    # SOFTWARE
    # --------------------------------------------------

    if (
        "software" in role
        or "software engineer" in role
        or "developer" in role
    ):
        keywords.extend([
            "Software Engineer",
            "Software Developer",
        ])

    # --------------------------------------------------
    # BACKEND
    # --------------------------------------------------

    if (
        "backend" in role
        or "back end" in role
    ):
        keywords.extend([
            "Backend Engineer",
            "Backend Developer",
        ])

    # --------------------------------------------------
    # FRONTEND
    # --------------------------------------------------

    if (
        "frontend" in role
        or "front end" in role
    ):
        keywords.extend([
            "Frontend Engineer",
            "Frontend Developer",
        ])

    # --------------------------------------------------
    # DEVOPS
    # --------------------------------------------------

    if "devops" in role:
        keywords.extend([
            "DevOps Engineer",
            "Cloud Engineer",
        ])

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    return list(dict.fromkeys(
        keyword.strip()
        for keyword in keywords
        if keyword and keyword.strip()
    ))