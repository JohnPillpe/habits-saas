from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HabitCreate(BaseModel):
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
