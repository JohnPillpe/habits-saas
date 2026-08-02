def build_career_advice(
    skill_gap: dict,
    market_report: str,
    preference,
):
    """
    Genera un resumen profesional basado en el mercado
    y el perfil del usuario.
    """

    advice = []

    advice.append(
        f"Objetivo profesional: {preference.desired_role}"
    )

    advice.append("")

    advice.append(
        f"Tu compatibilidad actual con el mercado es del {skill_gap['current_match']}%."
    )

    advice.append("")

    if skill_gap["market_strengths"]:

        advice.append("Fortalezas:")

        for skill in skill_gap["market_strengths"]:
            advice.append(f"• {skill}")

        advice.append("")

    if skill_gap["missing_skills"]:

        advice.append("Prioridad de aprendizaje:")

        for skill in skill_gap["recommended_order"]:
            advice.append(f"• {skill}")

        advice.append("")

    advice.append("Resumen del mercado:")

    advice.append(market_report)

    return "\n".join(advice)