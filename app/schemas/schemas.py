from datetime import datetime
from typing import Literal, Any

from pydantic import BaseModel, ConfigDict


class HabitCreate(BaseModel):
    nombre: str
    descripcion: str | None = None


class HabitUpdate(BaseModel):
    nombre: str
    descripcion: str | None = None


class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    creado_en: datetime
    racha_actual: int
    total_completados: int
    ultimo_registro: str | None


class UsuarioCreate(BaseModel):
    email: str
    password: str


class UsuarioLogin(BaseModel):
    email: str
    password: str


class UsuarioResponse(BaseModel):
    id: int
    email: str
    creado_en: datetime

    class Config:
        from_attributes = True

class AgentResponse(BaseModel):
    type: Literal[
        "text",
        "habit_created",
        "habit_completed",
        "habit_deleted",
        "jobs_found",
        "error",
    ]

    message: str

    data: Any | None = None