import os
import json

from fastapi import HTTPException
from openai import OpenAI
api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

from app.models.models import Habit

from app.agents.tools import TOOLS_MAP
from app.schemas.schemas import AgentResponse

TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "crear_habito",
            "description": "Crea un nuevo hábito. Úsalo cuando el usuario pida añadir/crear un hábito.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string", "description": "Nombre del hábito"},
                    "descripcion": {"type": "string", "description": "Descripción opcional"},
                },
                "required": ["nombre"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "completar_habito",
            "description": "Marca un hábito como completado hoy. Úsalo cuando el usuario diga que completó un hábito.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string", "description": "Nombre exacto del hábito"},
                },
                "required": ["nombre"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "eliminar_habito",
            "description": "Elimina un hábito. Úsalo cuando el usuario pida borrar/eliminar un hábito.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string", "description": "Nombre exacto del hábito"},
                },
                "required": ["nombre"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "scrapear_ofertas",
            "description":"Busca ofertas de trabajo reales en Remotive usando una tecnología o puesto. Usa esta herramienta cuando el usuario pida buscar empleos u ofertas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "palabra": {
                        "type": "string",
                        "description": "Tecnología o puesto a buscar"
                    }
                },
                "required": ["palabra"]
            }
        }
    },

        {
    "type": "function",
    "function": {
        "name": "consultar_documento",
        "description": "Busca información en los documentos PDF del usuario. Usa esta herramienta cuando el usuario pregunte sobre el contenido de documentos que ha subido.",
        "parameters": {
            "type": "object",
            "properties": {
                "consulta": {
                    "type": "string",
                    "description": "Pregunta del usuario sobre sus documentos"
                }
            },
            "required": ["consulta"]
        }
    }
},       

]   

def ejecutar_agente(
    consulta: str,
    db,
    usuario
):

    # Obtener hábitos del usuario para contexto
    habitos = db.query(Habit).filter(Habit.usuario_id == usuario.id).all()
    nombres = [h.nombre for h in habitos]
    context = f"Tienes estos hábitos: {', '.join(nombres) if nombres else 'ninguno'}."
    messages = [
        {"role": "system", "content": "Eres un asistente que ayuda con hábitos. Puedes crear, completar, eliminar hábitos y buscar ofertas de trabajo usando herramientas. Usa las herramientas cuando el usuario pida acciones."},
        {"role": "user", "content": f"{context}\n\nPregunta: {consulta}"}
    ]

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY no configurada")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOLS_SPEC,
        tool_choice="auto",
    )

    message = response.choices[0].message

    # Si la IA quiere llamar una herramienta
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name in TOOLS_MAP:
                result = TOOLS_MAP[function_name](**function_args, db=db, usuario=usuario)

                tipos = {
                    "crear_habito": "habit_created",
                    "completar_habito": "habit_completed",
                    "eliminar_habito": "habit_deleted",
                    "scrapear_ofertas": "jobs_found",
                 }

                return AgentResponse(
                    type=tipos.get(function_name, "text"),
                    message=result,
                    data=None
                )
                
            else:
                return AgentResponse(
                    type="error",
                    message="❌ Herramienta no disponible."
                )

    # Si la IA no llama a ninguna herramienta, devuelve su respuesta textual
    return AgentResponse(
        type="text",
        message=message.content
    )