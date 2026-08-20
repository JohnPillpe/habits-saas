from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Usuario

from app.schemas.schemas import (
    UsuarioCreate,
    UsuarioResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
)

from app.core.auth import (
    hashear_password,
    verificar_password,
    crear_token,
    get_current_user,
)

from app.services.password_reset_service import (
    request_password_reset,
    reset_password,
    change_password,
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=201,
)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
):

    existe = (
        db.query(Usuario)
        .filter(
            Usuario.email == usuario.email
        )
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado",
        )

    nuevo = Usuario(
        email=usuario.email,
        password_hash=hashear_password(
            usuario.password
        ),
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    db_usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == form_data.username
        )
        .first()
    )

    if not db_usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario incorrecto",
        )

    if not verificar_password(
        form_data.password,
        db_usuario.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta",
        )

    token = crear_token(
        {
            "sub": db_usuario.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):

    request_password_reset(
        request.email,
        db,
    )

    return {
        "message": (
            "If an account exists with this email, "
            "a password reset link has been sent."
        )
    }


@router.post("/reset-password")
def reset_password_endpoint(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):

    if len(request.password) < 8:
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must contain at least 8 characters."
            ),
        )

    try:
        reset_password(
            request.token,
            request.password,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return {
        "message": (
            "Password updated successfully. "
            "You can now log in."
        )
    }


@router.post("/change-password")
def change_password_endpoint(
    request: ChangePasswordRequest,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:
        change_password(
            usuario,
            request.current_password,
            request.new_password,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return {
        "message": "Password changed successfully."
    }