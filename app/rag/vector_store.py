import uuid
import chromadb

from app.rag.embeddings import generar_embeddings

_cliente = None
_collection = None


def get_collection():
    global _cliente, _collection

    if _cliente is None:
        _cliente = chromadb.PersistentClient(path="./chroma_db")

        _collection = _cliente.get_or_create_collection(
            name="documentos_rag",
            metadata={"hnsw:space": "cosine"}
        )

    return _collection


def guardar_fragmentos(
    usuario_id: int,
    nombre_documento: str,
    fragmentos: list[str],
):
    collection = get_collection()

    if not fragmentos:
        return

    embeddings = generar_embeddings(fragmentos)

    ids = [str(uuid.uuid4()) for _ in fragmentos]

    metadatas = [
        {
            "usuario_id": usuario_id,
            "documento": nombre_documento,
            "fragmento": i,
        }
        for i in range(len(fragmentos))
    ]

    collection.add(
        ids=ids,
        documents=fragmentos,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def buscar_fragmentos(
    usuario_id: int,
    consulta: str,
    n_resultados: int = 5,
):
    collection = get_collection()

    embedding = generar_embeddings([consulta])

    resultados = collection.query(
        query_embeddings=embedding,
        n_results=n_resultados,
        where={"usuario_id": usuario_id},
    )

    if (
        resultados["documents"]
        and len(resultados["documents"][0]) > 0
    ):
        return resultados["documents"][0]

    return []

def obtener_documento_completo(
    usuario_id: int,
    nombre_documento: str,
):
    collection = get_collection()

    resultados = collection.get(
        where={
            "usuario_id": usuario_id,
            "documento": nombre_documento,
        },
        include=["documents", "metadatas"],
    )

    if not resultados["documents"]:
        return ""

    pares = list(
        zip(
            resultados["documents"],
            resultados["metadatas"],
        )
    )

    pares.sort(
        key=lambda x: x[1]["fragmento"]
    )

    texto = "\n\n".join(
        doc for doc, _ in pares
    )

    return texto

def eliminar_documento(
    usuario_id: int,
    nombre_documento: str,
):
    collection = get_collection()

    resultados = collection.get(
        where={
            "$and": [
                {"usuario_id": usuario_id},
                {"documento": nombre_documento},
            ]
        }
     
    )

    ids = resultados.get("ids", [])

    if ids:
        collection.delete(ids=ids)

    return len(ids)