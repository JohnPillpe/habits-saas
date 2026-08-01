from sentence_transformers import SentenceTransformer

_modelo = None


def get_embedding_model():
    global _modelo

    if _modelo is None:
        _modelo = SentenceTransformer("all-MiniLM-L6-v2")

    return _modelo


def generar_embeddings(textos: list[str]) -> list[list[float]]:
    """
    Convierte una lista de textos en embeddings.
    """
    modelo = get_embedding_model()

    embeddings = modelo.encode(textos)

    return embeddings.tolist()
