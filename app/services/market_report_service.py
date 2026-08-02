def build_market_report(analysis):
    """
    Convierte el análisis estadístico del mercado
    en un informe legible por el agente.
    """

    report = []

    report.append("=== MARKET REPORT ===")
    report.append(f"Total jobs: {analysis['total_jobs']}")

    if analysis["companies"]:
        report.append("")
        report.append("Top companies:")
        for company, count in analysis["companies"][:5]:
            report.append(f"- {company} ({count})")

    if analysis["categories"]:
        report.append("")
        report.append("Top categories:")
        for category, count in analysis["categories"][:5]:
            report.append(f"- {category} ({count})")

    if analysis["skills"]:
        report.append("")
        report.append("Most requested skills:")
        for skill, count in analysis["skills"][:10]:
            report.append(f"- {skill} ({count})")

    if analysis["countries"]:
        report.append("")
        report.append("Countries:")
        for country, count in analysis["countries"][:10]:
            report.append(f"- {country} ({count})")

    if analysis["salaries"]:
        report.append("")
        report.append("Salary examples:")
        for salary in analysis["salaries"][:5]:
            report.append(f"- {salary}")

    return "\n".join(report)