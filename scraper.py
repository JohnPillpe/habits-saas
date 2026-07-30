import requests
from typing import List, Dict


def buscar_ofertas_remotive(
    palabra: str,
    max_ofertas: int = 5
) -> List[Dict[str, str]]:
    """
    Busca ofertas de empleo en Remotive usando su API pública.
    """

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": palabra,
        "limit": max_ofertas
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        ofertas = []

        for job in data.get("jobs", [])[:max_ofertas]:

            ofertas.append({
                "titulo": job.get("title", "Sin título"),
                "empresa": job.get("company_name", "No especificada"),
                "categoria": job.get("category", "No especificada"),
                "salario": job.get("salary", "No especificado"),
                "tags": ", ".join(job.get("tags", [])[:5]),
                "enlace": job.get("url", "")
            })

        return ofertas


    except requests.RequestException as e:

        return [
            {
                "error": f"Error conectando con Remotive: {str(e)}"
            }
        ]       


