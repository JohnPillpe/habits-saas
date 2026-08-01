import io
import pypdf


def extraer_texto_pdf(contenido_bytes: bytes) -> str:
    """
    Extrae todo el texto de un PDF.
    """

    reader = pypdf.PdfReader(io.BytesIO(contenido_bytes))

    texto = ""

    for pagina in reader.pages:

        pagina_texto = pagina.extract_text()

        if pagina_texto:
            texto += pagina_texto + "\n"

    return texto


def dividir_en_fragmentos(
    texto: str,
    tamano_chunk: int = 500,
):
    """
    Divide un texto largo en fragmentos.
    """

    if not texto.strip():
        return []

    fragmentos = []

    inicio = 0

    while inicio < len(texto):

        fin = inicio + tamano_chunk

        fragmentos.append(
            texto[inicio:fin]
        )

        inicio = fin

    return fragmentos