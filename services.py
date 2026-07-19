from datetime import date, timedelta

from sqlalchemy.orm import Session

from models import Habit, Registro


def calcular_racha(fechas_completadas: set[date]) -> int:
    if not fechas_completadas:
        return 0

    hoy = date.today()
    actual = hoy if hoy in fechas_completadas else hoy - timedelta(days=1)

    racha = 0
    while actual in fechas_completadas:
        racha += 1
        actual -= timedelta(days=1)

    return racha


def obtener_estadisticas_habito(habito: Habit) -> tuple[int, int]:
    fechas_completadas = {
        registro.fecha
        for registro in habito.registros
        if registro.completado
    }
    total = len(fechas_completadas)
    racha = calcular_racha(fechas_completadas)
    return racha, total


def habit_to_response(habito: Habit) -> dict:
    racha, total = obtener_estadisticas_habito(habito)

    ultimo = None

    if habito.registros:
        fechas = [
            registro.fecha
            for registro in habito.registros
            if registro.completado
        ]

        if fechas:
            ultimo = max(fechas).isoformat()

    return {
        "id": habito.id,
        "nombre": habito.nombre,
        "descripcion": habito.descripcion,
        "creado_en": habito.creado_en,
        "racha_actual": racha,
        "total_completados": total,
        "ultimo_registro": ultimo,
    }


def marcar_completado_hoy(db: Session, habito_id: int) -> bool:
    habito = db.query(Habit).filter(Habit.id == habito_id).first()
    if not habito:
        return False

    hoy = date.today()
    registro_existente = (
        db.query(Registro)
        .filter(
            Registro.habitos_id == habito_id,
            Registro.fecha == hoy,
            Registro.completado.is_(True),
        )
        .first()
    )

    if registro_existente:
        return True

    db.add(
        Registro(
            habitos_id=habito_id,
            fecha=hoy,
            completado=True,
        )
    )
    db.commit()
    return True
