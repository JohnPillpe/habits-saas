from sqlalchemy.orm import Session

from app.core.auth import (
    crear_token_reset_password,
    verificar_token_reset_password,
    hashear_password,
    verificar_password,
)

from app.models.models import Usuario

from app.services.email_service import (
    send_password_reset_email,
)


def request_password_reset(
    email: str,
    db: Session,
):
    normalized_email = email.strip().lower()

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == normalized_email
        )
        .first()
    )

    # Do not reveal whether the email exists.
    if not usuario:
        return

    token = crear_token_reset_password(
        usuario.email
    )

    send_password_reset_email(
        usuario.email,
        token,
    )


def reset_password(
    token: str,
    password: str,
    db: Session,
):
    email = verificar_token_reset_password(
        token
    )

    if not email:
        raise ValueError(
            "Invalid or expired password reset link."
        )

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == email
        )
        .first()
    )

    if not usuario:
        raise ValueError(
            "User not found."
        )

    usuario.password_hash = hashear_password(
        password
    )

    db.commit()

    return usuario


def change_password(
    usuario: Usuario,
    current_password: str,
    new_password: str,
    db: Session,
):
    if not verificar_password(
        current_password,
        usuario.password_hash,
    ):
        raise ValueError(
            "Current password is incorrect."
        )

    if len(new_password) < 8:
        raise ValueError(
            "New password must contain at least 8 characters."
        )

    usuario.password_hash = hashear_password(
        new_password
    )

    db.commit()
    db.refresh(usuario)

    return usuario