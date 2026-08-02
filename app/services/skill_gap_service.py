from collections import Counter

def analyze_skill_gap(
    cv_text: str,
    market_analysis: dict,
):
    """
    Compara el CV del usuario contra las habilidades
    más demandadas del mercado.
    """

    skills = market_analysis.get("skills", [])

    if not skills:
        return {
            "current_match": 0,
            "missing_skills": [],
            "recommended_order": [],
            "market_strengths": [],
        }

    market_skills = []

    for skill, count in skills:
        market_skills.append(skill.lower())

    cv_lower = cv_text.lower()

    present = []
    missing = []

    for skill in market_skills:
        if skill in cv_lower:
            present.append(skill)
        else:
            missing.append(skill)

    if market_skills:
        match = int(
            len(present) / len(market_skills) * 100
        )
    else:
        match = 0

    return {
        "current_match": match,
        "missing_skills": missing,
        "recommended_order": missing,
        "market_strengths": present,
    }