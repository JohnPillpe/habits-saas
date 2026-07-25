from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from database import get_db, Base, engine
from models import Habit, Usuario, Registro
from schemas import (
    HabitCreate,
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
    usuario: UsuarioLogin,
    db: Session = Depends(get_db)
):

    db_usuario = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()


    if not db_usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario incorrecto"
        )


    if not verificar_password(
        usuario.password,
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


    nuevo_registro = Registro(
        habitos_id=habito.id,
        fecha=date.today(),
        completado=True
    )


    db.add(nuevo_registro)
    db.commit()


    return {
        "message": "Hábito completado"
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