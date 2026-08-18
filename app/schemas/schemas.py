from datetime import datetime

from pydantic import BaseModel, ConfigDict



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

class UserJobPreferenceCreate(BaseModel):
    desired_role: str
    target_countries: list[str]
    target_cities: list[str]
    remote: bool = True
    hybrid: bool = False
    onsite: bool = False
    published_within_days: int = 7


class UserJobPreferenceResponse(UserJobPreferenceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str