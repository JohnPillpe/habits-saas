from collections import Counter


def analyze_market(jobs: list):
    """
    Analiza todas las ofertas obtenidas de los distintos proveedores.
    Devuelve estadísticas del mercado.
    """

    companies = Counter()
    countries = Counter()
    categories = Counter()
    skills = Counter()

    salaries = []

    for job in jobs:

        companies[job.get("empresa", "Unknown")] += 1

        categories[job.get("categoria", "Unknown")] += 1

        country = job.get("pais")

        if country:
            countries[country] += 1

        tags = job.get("tags", "")

        if isinstance(tags, str):

            for tag in tags.split(","):

                tag = tag.strip()

                if tag:
                    skills[tag] += 1

        salary = job.get("salario")

        if salary:
            salaries.append(salary)

    return {
        "total_jobs": len(jobs),
        "companies": companies.most_common(20),
        "countries": countries.most_common(20),
        "categories": categories.most_common(20),
        "skills": skills.most_common(50),
        "salaries": salaries,
    }