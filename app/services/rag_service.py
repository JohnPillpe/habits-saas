import os

from openai import OpenAI

from app.rag.vector_store import buscar_fragmentos


def answer_query(
    consulta: str,
    usuario_id: int,
) -> str:
    """
    Busca información en los documentos del usuario
    y genera una respuesta utilizando DeepSeek.
    """

    fragmentos = buscar_fragmentos(
        usuario_id,
        consulta,
        n_resultados=5,
    )

def get_cv_text(
    usuario_id: int,
) -> str:
    """
    Recupera el texto del CV del usuario desde el vector store.
    """

    fragmentos = buscar_fragmentos(
        usuario_id,
        "curriculum vitae cv resume experiencia habilidades",
        n_resultados=30,
    )

    if not fragmentos:
        return ""

    return "\n".join(fragmentos)



    if not fragmentos:
        return "No encontré información relacionada en tus documentos."

    contexto = "\n\n---\n\n".join(fragmentos)

    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        return "DEEPSEEK_API_KEY no configurada."

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
    )

    prompt = f"""
Eres un asistente que responde EXCLUSIVAMENTE usando el contexto.

Si la respuesta no aparece en el contexto,
responde exactamente:

"No encontré información sobre eso en tus documentos."

Contexto:

{contexto}

Pregunta:

{consulta}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "Responde únicamente usando el contexto proporcionado."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=400,
    )

    return response.choices[0].message.content