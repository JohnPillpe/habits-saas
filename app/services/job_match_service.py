def calculate_match_score(
    job,
    skill_gap,
    preference,
):
    score = skill_gap["current_match"]

    title = job.get("titulo", "").lower()
    category = job.get("categoria", "").lower()
    tags = job.get("tags", "").lower()

    job_text = f"{title} {category} {tags}"

    # =========
    # PREFERENCIAS
    # =========

    if preference:

        # Modalidad

        if preference.remote and "remote" in job_text:
            score += 20

        if preference.hybrid and "hybrid" in job_text:
            score += 20

        if preference.onsite and (
            "on-site" in job_text
            or "onsite" in job_text
        ):
            score += 20

        # Países

        for country in preference.target_countries or []:

            if country.lower() in job_text:
                score += 15
                break

        # Rol

        role = preference.desired_role.lower()

        if role in job_text:
            score += 30

    # =========
    # SKILLS DEL CV
    # =========

    for skill in skill_gap["market_strengths"]:

        if skill in job_text:
            score += 8

    for skill in skill_gap["missing_skills"]:

        if skill in job_text:
            score -= 5

    score = max(0, min(score, 100))

    return score