from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Habit, Usuario, Registro
from app.schemas.schemas import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
)
from app.services.services import (
    habit_to_response,
    marcar_completado_hoy,
)
from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.get("")
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





@router.post("")
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

@router.put("/{habito_id}")
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




@router.post("/{habito_id}/complete")
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

@router.delete("/{habito_id}")
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