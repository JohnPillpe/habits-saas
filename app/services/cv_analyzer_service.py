def analyze_cv(
    cv_text: str,
    market_analysis: dict,
    skill_gap: dict,
):

    score = skill_gap["current_match"]

    strengths = []

    weaknesses = []

    recommendations = []

    if score >= 80:
        strengths.append(
            "Tu CV está bastante alineado con el mercado."
        )

    elif score >= 60:
        strengths.append(
            "Tu perfil tiene una buena base."
        )
        weaknesses.append(
            "Aún faltan varias habilidades demandadas."
        )

    else:
        weaknesses.append(
            "Tu CV necesita mejoras importantes para competir."
        )

    for skill in skill_gap["missing_skills"][:5]:
        recommendations.append(
            f"Aprender {skill}"
        )

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
    }