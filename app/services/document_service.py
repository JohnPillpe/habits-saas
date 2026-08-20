from sqlalchemy.orm import Session

from app.models.models import Document


def guardar_documento(
    db: Session,
    usuario_id: int,
    nombre: str,
    tipo: str,
):
    documento = Document(
        usuario_id=usuario_id,
        nombre=nombre,
        tipo=tipo,
    )

    db.add(documento)
    db.commit()
    db.refresh(documento)

    return documento


def listar_documentos(
    db: Session,
    usuario_id: int,
):
    return (
        db.query(Document)
        .filter(Document.usuario_id == usuario_id)
        .order_by(Document.fecha_subida.desc())
        .all()
    )


def listar_cvs(
    db: Session,
    usuario_id: int,
):
    return (
        db.query(Document)
        .filter(
            Document.usuario_id == usuario_id,
            Document.tipo == "cv",
        )
        .order_by(Document.fecha_subida.desc())
        .all()
    )


def buscar_documento(
    db: Session,
    documento_id: int,
    usuario_id: int,
):
    return (
        db.query(Document)
        .filter(
            Document.id == documento_id,
            Document.usuario_id == usuario_id,
        )
        .first()
    )


def eliminar_documento(
    db: Session,
    documento_id: int,
    usuario_id: int,
):
    documento = buscar_documento(
        db,
        documento_id,
        usuario_id,
    )

    if not documento:
        return None

    db.delete(documento)
    db.commit()

    return documento