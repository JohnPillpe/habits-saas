from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from database import get_db, Base, engine
from models import Habit, Usuario, Registro
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
        "completados_por_dia": completados_por_dia,
        "racha_por_habito": racha_por_habito,
        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "fecha_fin": hoy.strftime("%Y-%m-%d")
    }

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