from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import obtener_usuario_actual
from app.models.models import Usuario
from app.agents.agent import ejecutar_agente

router = APIRouter()


class RecomendacionRequest(BaseModel):
    consulta: str


@router.post("/api/ai/recommend")
async def recomendar(
    request: RecomendacionRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):

    resultado = ejecutar_agente(
        request.consulta,
        db,
        usuario,
    )

    return resultado.model_dump()