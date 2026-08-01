from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Usuario
from app.schemas.schemas import (
    UsuarioCreate,
    UsuarioResponse,
)
from app.core.auth import (
    hashear_password,
    verificar_password,
    crear_token,
)

router = APIRouter()


@router.post("/register", response_model=UsuarioResponse, status_code=201)
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

@router.post("/login")
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