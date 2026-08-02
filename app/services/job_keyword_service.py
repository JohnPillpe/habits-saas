def build_search_keywords(role: str) -> list[str]:
    """
    Convierte un rol en varias búsquedas útiles.
    """

    role = role.lower()

    keywords = []

    if "python" in role:
        keywords.extend([
            "Python",
            "FastAPI",
            "Django",
            "Backend",
        ])

    if "ai" in role:
        keywords.extend([
            "AI",
            "Machine Learning",
            "LLM",
        ])

    if "data" in role:
        keywords.extend([
            "Data Engineer",
            "Data Science",
        ])

    # añadir siempre el rol completo
    keywords.append(role)

    # eliminar duplicados
    return list(dict.fromkeys(keywords))