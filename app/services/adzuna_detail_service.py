import requests


def get_full_adzuna_description(
    adzuna_url: str | None,
) -> str | None:
    """
    Intenta recuperar una descripción completa
    desde la URL original de Adzuna.

    IMPORTANTE:

    Un 404 NO es un error fatal.

    Adzuna puede devolver resultados de búsqueda
    cuyo anuncio ya no está disponible mediante
    el endpoint/página de detalle.

    En ese caso devolvemos None y el provider
    utilizará la descripción proporcionada por
    la API de búsqueda.
    """

    if not adzuna_url:
        return None

    url = str(
        adzuna_url
    ).strip()

    if not url:
        return None

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0 Safari/537.36"
                )
            },
        )

        # --------------------------------------------------
        # 404
        # --------------------------------------------------

        if response.status_code == 404:

            print(
                "[ADZUNA] "
                "Detail page returned HTTP 404. "
                "Using API description."
            )

            return None

        # --------------------------------------------------
        # OTHER HTTP ERRORS
        # --------------------------------------------------

        if response.status_code >= 400:

            print(
                "[ADZUNA] "
                f"Detail page returned HTTP "
                f"{response.status_code}. "
                "Using API description."
            )

            return None

        html = (
            response.text
            or ""
        )

        if not html.strip():
            return None

        description = (
            _extract_description(
                html
            )
        )

        if not description:
            return None

        return description

    except requests.RequestException as e:

        print(
            "[ADZUNA] "
            f"Detail request failed: {str(e)}"
        )

        return None

    except Exception as e:

        print(
            "[ADZUNA] "
            f"Unexpected detail parsing error: "
            f"{str(e)}"
        )

        return None


def _extract_description(html: str) -> str | None:
    """
    Extrae una descripción si existe
    en el HTML de la página.

    Este parser es deliberadamente conservador.
    Si no encuentra una descripción fiable,
    devuelve None.
    """

    from html import unescape
    import re

    text = html

    # Elimina scripts/styles.
    text = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    text = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Elimina tags HTML.
    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
    )

    text = unescape(
        text
    )

    # Normaliza espacios.
    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    if not text:
        return None

    # Evitamos devolver páginas enteras
    # como si fueran una descripción.
    markers = [
        "Job description",
        "About this role",
        "About the role",
        "What you'll do",
        "What you’ll do",
        "The role",
        "Description",
    ]

    for marker in markers:

        index = text.lower().find(
            marker.lower()
        )

        if index == -1:
            continue

        extracted = text[
            index:
        ].strip()

        if len(extracted) >= 150:

            return extracted[
                :12000
            ]

    return None