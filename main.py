from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from scraper import buscar_ofertas_remotive


import os
import json
from openai import OpenAI

from pydantic import BaseModel

from database import get_db, Base, engine
from models import Habit, Usuario, Registro, JobOffer
from schemas import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse
)



from services import habit_to_response, marcar_completado_hoy
from auth import (
    hashear_password,
    verificar_password,
    crear_token,
    obtener_usuario_actual
)




app = FastAPI(title="Seguimiento de Hábitos")   

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)



# =========================
# AUTENTICACIÓN
# =========================


@app.post("/register", response_model=UsuarioResponse, status_code=201)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    existe = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )


    nuevo = Usuario(
        email=usuario.email,
        password_hash=hashear_password(usuario.password)
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo



@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_usuario = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()


    if not db_usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario incorrecto"
        )


    if not verificar_password(
        form_data.password,
        db_usuario.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )


    token = crear_token(
        {
            "sub": db_usuario.email
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }





# =========================
# HABITOS
# =========================


@app.get("/habits", response_model=list[HabitResponse])
def listar_habitos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    habitos = db.query(Habit).filter(
        Habit.usuario_id == usuario.id
    ).all()


    return [
        habit_to_response(h)
        for h in habitos
    ]





@app.post("/habits", response_model=HabitResponse, status_code=201)
def crear_habito(
    habito: HabitCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    nuevo = Habit(
        nombre=habito.nombre,
        descripcion=habito.descripcion,
        usuario_id=usuario.id
    )


    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)


    return habit_to_response(nuevo)

@app.put("/habits/{habito_id}", response_model=HabitResponse)
def editar_habito(
    habito_id: int,
    datos: HabitUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    habito = db.query(Habit).filter(
        Habit.id == habito_id,
        
        Habit.usuario_id == usuario.id
    ).first()

    if not habito:
        raise HTTPException(
            status_code=404,
            detail="Hábito no encontrado"
        )

    habito.nombre = datos.nombre
    habito.descripcion = datos.descripcion

    db.commit()
    db.refresh(habito)

    return habit_to_response(habito)




@app.post("/habits/{habito_id}/complete")
def completar_habito(
    habito_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    resultado = marcar_completado_hoy(db, habito_id)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Hábito no encontrado"
        )

    return {
        "message": "Hábito completado"
    }

@app.delete("/habits/{habito_id}")
def eliminar_habito(
    habito_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    habito = db.query(Habit).filter(
        Habit.id == habito_id,
        Habit.usuario_id == usuario.id
    ).first()

    if not habito:
        raise HTTPException(
            status_code=404,
            detail="Hábito no encontrado"
        )


    db.query(Registro).filter(
        Registro.habitos_id == habito.id
    ).delete()

    db.delete(habito)
    db.commit()

    return {
        "message": "Hábito eliminado"
    } 

@app.get("/job-offers")
def listar_ofertas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):

    ofertas = db.query(JobOffer).filter(
        JobOffer.usuario_id == usuario.id
    ).all()

    return ofertas  

@app.get("/api/stats")
def obtener_estadisticas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    from datetime import datetime, timedelta
    import calendar
    
    hoy = datetime.now().date()
    
    # 1. Obtener todos los hábitos del usuario
    habitos = db.query(Habit).filter(Habit.usuario_id == usuario.id).all()
    habitos_ids = [h.id for h in habitos]
    
    # 2. Obtener registros de los últimos 7 días
    fecha_inicio = hoy - timedelta(days=6)
    registros = db.query(Registro).filter(
        Registro.habitos_id.in_(habitos_ids),
        Registro.fecha >= fecha_inicio
    ).all()
    
    # 3. Calcular completados por día
    completados_por_dia = {}
    for i in range(7):
        fecha = fecha_inicio + timedelta(days=i)
        completados_por_dia[fecha.strftime("%Y-%m-%d")] = 0
    
    for registro in registros:
        fecha_str = registro.fecha.strftime("%Y-%m-%d")
        if fecha_str in completados_por_dia:
            completados_por_dia[fecha_str] += 1
    
    # 4. Calcular racha total
    racha_total = 0
    fecha_actual = hoy

    while True:
        fecha_str = fecha_actual.strftime("%Y-%m-%d")

        completados_hoy = db.query(Registro).filter(
            Registro.habitos_id.in_(habitos_ids),
            Registro.fecha == fecha_actual
        ).count()

        if completados_hoy > 0:
            racha_total += 1
            fecha_actual -= timedelta(days=1)
        else:
            break


    # NUEVO: días con actividad
    dias_activos = db.query(Registro.fecha).filter(
        Registro.habitos_id.in_(habitos_ids)
    ).distinct().count()


    # 5. Calcular racha por hábito
    racha_por_habito = []
    for habito in habitos:
        fechas_completadas = [r.fecha for r in db.query(Registro).filter(
            Registro.habitos_id == habito.id
        ).order_by(Registro.fecha.desc()).all()]
        
        racha = 0
        fecha = hoy
        while True:
            if fecha in fechas_completadas:
                racha += 1
                fecha -= timedelta(days=1)
            else:
                break
        racha_por_habito.append({
            "nombre": habito.nombre,
            "racha": racha,
            "total": len(fechas_completadas)
        })
    
    return {
        "racha_total": racha_total,
        "total_habitos": len(habitos),
        "dias_activos": dias_activos,
        "completados_por_dia": completados_por_dia,
        "racha_por_habito": racha_por_habito,
        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "fecha_fin": hoy.strftime("%Y-%m-%d")
    }


class RecomendacionRequest(BaseModel):
    consulta: str

# ==========================================
# HERRAMIENTAS PARA EL AGENTE (FUNCTION CALLING)
# ==========================================

def tool_crear_habito(nombre: str, descripcion: str = None, db=None, usuario=None):
    """Crea un nuevo hábito para el usuario autenticado."""
    nuevo = Habit(nombre=nombre, descripcion=descripcion, usuario_id=usuario.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return f"✅ Hábito '{nombre}' creado con éxito."

def tool_completar_habito(nombre: str, db=None, usuario=None):
    """Marca un hábito como completado HOY (busca por nombre exacto)."""
    habito = db.query(Habit).filter(Habit.nombre == nombre, Habit.usuario_id == usuario.id).first()
    if not habito:
        return f"❌ No encontré el hábito '{nombre}'."
    from services import marcar_completado_hoy
    marcar_completado_hoy(db, habito.id)
    return f"✅ Hábito '{nombre}' completado hoy."

def tool_eliminar_habito(nombre: str, db=None, usuario=None):
    """Elimina un hábito (busca por nombre exacto)."""
    habito = db.query(Habit).filter(Habit.nombre == nombre, Habit.usuario_id == usuario.id).first()
    if not habito:
        return f"❌ No encontré el hábito '{nombre}'."
    db.delete(habito)
    db.commit()
    return f"🗑️ Hábito '{nombre}' eliminado."

def tool_scrapear_ofertas(palabra: str, db=None, usuario=None):
    """Busca ofertas reales en Remotive y las guarda en PostgreSQL."""

    ofertas = buscar_ofertas_remotive(
        palabra,
        max_ofertas=5
    )

    if not ofertas:
        return f"No encontré ofertas para {palabra}"

    if "error" in ofertas[0]:
        return ofertas[0]["error"]

    nuevas_guardadas = 0
    resultado = ""

    for i, oferta in enumerate(ofertas, 1):

        resultado += f"""
    {i}. {oferta['titulo']}
    Empresa: {oferta['empresa']}
    Categoría: {oferta['categoria']}
    Salario: {oferta['salario']}
    Tags: {oferta['tags']}
    Link: {oferta['enlace']}

    """

        existe = db.query(JobOffer).filter(
            JobOffer.enlace == oferta["enlace"],
            JobOffer.usuario_id == usuario.id
        ).first()

        if existe:
            continue

        nueva_oferta = JobOffer(
            titulo=oferta["titulo"],
            empresa=oferta["empresa"],
            categoria=oferta["categoria"],
            salario=oferta["salario"],
            tags=oferta["tags"],
            enlace=oferta["enlace"],
            usuario_id=usuario.id
        )

        db.add(nueva_oferta)
        nuevas_guardadas += 1

    db.commit()

    nombre_habito = f"Revisar ofertas de {palabra}"

    existe = db.query(Habit).filter(
        Habit.nombre == nombre_habito,
        Habit.usuario_id == usuario.id
    ).first()

    if not existe:
        tool_crear_habito(
            nombre=nombre_habito,
            descripcion=f"{len(ofertas)} ofertas encontradas en Remotive",
            db=db,
            usuario=usuario
        )

    return (
        f"🔎 Encontradas: {len(ofertas)}\n"
        f"💾 Nuevas guardadas: {nuevas_guardadas}\n\n"
        + resultado
    )


TOOLS_MAP = {
    "crear_habito": tool_crear_habito,
    "completar_habito": tool_completar_habito,
    "eliminar_habito": tool_eliminar_habito,
    "scrapear_ofertas": tool_scrapear_ofertas,
}

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
    }        

]


@app.post("/api/ai/recommend")
async def agente_habitos(
    request: RecomendacionRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    # Obtener hábitos del usuario para contexto
    habitos = db.query(Habit).filter(Habit.usuario_id == usuario.id).all()
    nombres = [h.nombre for h in habitos]
    context = f"Tienes estos hábitos: {', '.join(nombres) if nombres else 'ninguno'}."

    messages = [
        {"role": "system", "content": "Eres un asistente que ayuda con hábitos. Puedes crear, completar, eliminar hábitos y buscar ofertas de trabajo usando herramientas. Usa las herramientas cuando el usuario pida acciones."},
        {"role": "user", "content": f"{context}\n\nPregunta: {request.consulta}"}
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
                return {"recomendacion": result}
            else:
                return {"recomendacion": "❌ Herramienta no disponible."}

    # Si la IA no llama a ninguna herramienta, devuelve su respuesta textual
    return {"recomendacion": message.content}


# =========================
# PAGINA WEB
# =========================



@app.get("/", response_class=HTMLResponse)
def pagina_principal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )