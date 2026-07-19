from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Habit(Base):
    __tablename__ = "habitos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    registros: Mapped[list["Registro"]] = relationship(
        "Registro", back_populates="habito", cascade="all, delete-orphan"
    )


class Registro(Base):
    __tablename__ = "registros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    habitos_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("habitos.id"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    completado: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    habito: Mapped["Habit"] = relationship("Habit", back_populates="registros")
