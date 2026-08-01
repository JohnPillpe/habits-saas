from app.rag.vector_store import get_collection


def obtener_cv(usuario_id: int) -> str:
    """
    Recupera todos los fragmentos del CV almacenados
    en ChromaDB y los une en un único texto.
    """

    collection = get_collection()

    resultados = collection.get(
        where={"usuario_id": usuario_id}
    )

    documentos = resultados.get("documents", [])

    if not documentos:
        return ""

    return "\n\n".join(documentos)