print("ESTOY CARGANDO stats.py")

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Habit, Registro, Usuario
from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/api/stats", tags=["Stats"])

@router.get("")
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